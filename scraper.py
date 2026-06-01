"""
ECAL Quick Commerce Scraper
Scrapes Blinkit, Zepto, and Swiggy Instamart for cigarette SKU availability
across selected Kolkata pin codes.

Usage:
    python scraper.py               # full run, all platforms & pin codes
    python scraper.py --platform blinkit
    python scraper.py --pincode 700019
    python scraper.py --debug       # non-headless, slow mode
"""

import asyncio
import json
import logging
import os
import re
import argparse
from datetime import datetime
from pathlib import Path
from typing import Optional

from playwright.async_api import async_playwright, Page, BrowserContext

from config import (
    PIN_CODES, SKUS, BRAND_SEARCH_TERMS,
    HEADLESS, SLOW_MO_MS, PAGE_TIMEOUT_MS, SEARCH_WAIT_MS,
    SCREENSHOT_ON_ERROR
)

# ─── Logging ──────────────────────────────────────────────────────────────────
LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)
DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)
SCREENSHOT_DIR = Path("screenshots")
SCREENSHOT_DIR.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-7s  %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(LOG_DIR / f"run_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"),
    ]
)
log = logging.getLogger(__name__)


# ─── Helpers ──────────────────────────────────────────────────────────────────

def normalise(text: str) -> str:
    """Lower-case, strip punctuation/extra spaces for fuzzy matching."""
    text = text.lower()
    text = re.sub(r"[&\-\./]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def sku_matched(sku_info: dict, product_text: str) -> bool:
    """Return True if product_text is a likely match for sku_info."""
    pt = normalise(product_text)
    for variant in sku_info["name_variants"]:
        if normalise(variant) in pt or pt in normalise(variant):
            return True
    # Looser: brand + pack-size check
    brand_norm = normalise(sku_info["brand"])
    sku_name_norm = normalise(sku_info["name"])
    # check if at least 3 words of the sku name appear in the product text
    words = [w for w in sku_name_norm.split() if len(w) > 2]
    match_count = sum(1 for w in words if w in pt)
    if match_count >= min(3, len(words)):
        return True
    return False


def load_results() -> dict:
    path = DATA_DIR / "results.json"
    if path.exists():
        with open(path) as f:
            return json.load(f)
    return {}


def save_results(results: dict):
    path = DATA_DIR / "results.json"
    with open(path, "w") as f:
        json.dump(results, f, indent=2)
    log.info(f"Results saved → {path}")


def init_result_structure() -> dict:
    """Build empty results skeleton."""
    return {
        "meta": {
            "last_run": None,
            "run_duration_s": None,
            "platforms": ["blinkit", "swiggy", "zepto"],
        },
        "data": {
            platform: {
                pin: {
                    sku["sku"]: {"available": None, "product_name_found": None, "error": None}
                    for sku in SKUS
                }
                for pin in PIN_CODES
            }
            for platform in ["blinkit", "swiggy", "zepto"]
        },
    }


# ─── BLINKIT ──────────────────────────────────────────────────────────────────

class BlinkitScraper:
    BASE_URL = "https://blinkit.com"
    NAME = "blinkit"

    def __init__(self, context: BrowserContext, debug: bool = False):
        self.context = context
        self.debug = debug

    async def _get_page(self) -> Page:
        page = await self.context.new_page()
        page.set_default_timeout(PAGE_TIMEOUT_MS)
        return page

    async def set_location(self, page: Page, pin_code: str) -> bool:
        """Set delivery pin code on Blinkit. Returns True on success."""
        try:
            await page.goto(self.BASE_URL, wait_until="domcontentloaded")
            await page.wait_for_timeout(2000)

            # Try clicking the location bar (several possible selectors)
            loc_selectors = [
                "[data-testid='location-bar']",
                "button:has-text('Delivery')",
                ".LocationBar",
                "header button",
                "[class*='location']",
                "input[placeholder*='Search']",
            ]
            clicked = False
            for sel in loc_selectors:
                try:
                    el = page.locator(sel).first
                    if await el.is_visible(timeout=2000):
                        await el.click()
                        clicked = True
                        break
                except Exception:
                    pass

            if not clicked:
                log.warning(f"Blinkit: could not open location picker for {pin_code}")
                return False

            await page.wait_for_timeout(1000)

            # Type pin code into the location search box
            input_sel = [
                "input[placeholder*='Search delivery']",
                "input[placeholder*='Enter your']",
                "input[placeholder*='Search']",
                "input[type='text']",
                "input[type='search']",
            ]
            for sel in input_sel:
                try:
                    inp = page.locator(sel).first
                    if await inp.is_visible(timeout=2000):
                        await inp.fill(pin_code)
                        await page.wait_for_timeout(SEARCH_WAIT_MS)
                        break
                except Exception:
                    pass

            # Click the first suggestion
            suggestion_sel = [
                "[data-testid='location-suggestion']",
                "[class*='suggestion']",
                "ul li",
                "[role='option']",
            ]
            for sel in suggestion_sel:
                try:
                    sug = page.locator(sel).first
                    if await sug.is_visible(timeout=2000):
                        await sug.click()
                        await page.wait_for_timeout(2000)
                        return True
                except Exception:
                    pass

            # Last resort: press Enter and hope
            await page.keyboard.press("Enter")
            await page.wait_for_timeout(2000)
            return True

        except Exception as e:
            log.error(f"Blinkit set_location({pin_code}): {e}")
            if SCREENSHOT_ON_ERROR:
                await page.screenshot(path=str(SCREENSHOT_DIR / f"blinkit_loc_{pin_code}.png"))
            return False

    async def search_brand(self, page: Page, brand: str) -> list[str]:
        """Search for a brand and return all product names visible in results."""
        try:
            query = brand.replace("&", "").replace(" ", "+")
            await page.goto(f"{self.BASE_URL}/s/?q={query}", wait_until="domcontentloaded")
            await page.wait_for_timeout(SEARCH_WAIT_MS)

            # Collect all product name texts on the page
            product_sel = [
                "[data-testid='product-name']",
                "[class*='ProductName']",
                "[class*='product-name']",
                "[class*='product_name']",
                "[class*='itemName']",
                "h3", "h4",
            ]
            names = []
            for sel in product_sel:
                try:
                    elements = await page.locator(sel).all()
                    for el in elements:
                        txt = (await el.inner_text()).strip()
                        if txt and len(txt) > 3:
                            names.append(txt)
                except Exception:
                    pass
            return list(set(names))  # dedupe

        except Exception as e:
            log.error(f"Blinkit search_brand({brand}): {e}")
            return []

    async def run_for_pincode(self, pin_code: str) -> dict:
        """Returns {sku_id: {available, product_name_found, error}} for one pin code."""
        result = {s["sku"]: {"available": False, "product_name_found": None, "error": None}
                  for s in SKUS}
        page = await self._get_page()
        try:
            ok = await self.set_location(page, pin_code)
            if not ok:
                for s in SKUS:
                    result[s["sku"]]["error"] = "location_failed"
                return result

            # Search per brand (batched)
            for brand, brand_queries in BRAND_SEARCH_TERMS.items():
                brand_skus = [s for s in SKUS if s["brand"] == brand]
                if not brand_skus:
                    continue
                found_names: list[str] = []
                for q in brand_queries:
                    names = await self.search_brand(page, q)
                    found_names.extend(names)
                    if names:
                        break  # first successful query is enough

                for sku in brand_skus:
                    for pname in found_names:
                        if sku_matched(sku, pname):
                            result[sku["sku"]]["available"] = True
                            result[sku["sku"]]["product_name_found"] = pname
                            break

                log.info(f"  Blinkit {pin_code} | {brand}: "
                         f"{sum(1 for s in brand_skus if result[s['sku']]['available'])}/"
                         f"{len(brand_skus)} found")

        except Exception as e:
            log.error(f"Blinkit run_for_pincode({pin_code}): {e}")
            if SCREENSHOT_ON_ERROR:
                await page.screenshot(path=str(SCREENSHOT_DIR / f"blinkit_{pin_code}_err.png"))
        finally:
            await page.close()
        return result


# ─── ZEPTO ────────────────────────────────────────────────────────────────────

class ZeptoScraper:
    BASE_URL = "https://www.zeptonow.com"
    NAME = "zepto"

    def __init__(self, context: BrowserContext, debug: bool = False):
        self.context = context
        self.debug = debug

    async def _get_page(self) -> Page:
        page = await self.context.new_page()
        page.set_default_timeout(PAGE_TIMEOUT_MS)
        return page

    async def set_location(self, page: Page, pin_code: str) -> bool:
        try:
            await page.goto(self.BASE_URL, wait_until="domcontentloaded")
            await page.wait_for_timeout(2000)

            loc_selectors = [
                "button:has-text('Deliver to')",
                "[class*='address']",
                "[data-testid*='location']",
                "header",
            ]
            for sel in loc_selectors:
                try:
                    el = page.locator(sel).first
                    if await el.is_visible(timeout=2000):
                        await el.click()
                        break
                except Exception:
                    pass

            await page.wait_for_timeout(1000)

            input_sel = [
                "input[placeholder*='Search']",
                "input[placeholder*='pincode']",
                "input[placeholder*='Enter']",
                "input[type='text']",
            ]
            for sel in input_sel:
                try:
                    inp = page.locator(sel).first
                    if await inp.is_visible(timeout=2000):
                        await inp.fill(pin_code)
                        await page.wait_for_timeout(SEARCH_WAIT_MS)
                        break
                except Exception:
                    pass

            # Try selecting suggestion
            sug_sel = [
                "[class*='suggestion']",
                "[data-testid*='suggestion']",
                "[role='option']",
                "ul li",
            ]
            for sel in sug_sel:
                try:
                    sug = page.locator(sel).first
                    if await sug.is_visible(timeout=2000):
                        await sug.click()
                        await page.wait_for_timeout(2000)
                        return True
                except Exception:
                    pass

            await page.keyboard.press("Enter")
            await page.wait_for_timeout(2000)
            return True

        except Exception as e:
            log.error(f"Zepto set_location({pin_code}): {e}")
            if SCREENSHOT_ON_ERROR:
                await page.screenshot(path=str(SCREENSHOT_DIR / f"zepto_loc_{pin_code}.png"))
            return False

    async def search_brand(self, page: Page, brand: str) -> list[str]:
        try:
            query = brand.replace("&", "").replace(" ", "+")
            await page.goto(f"{self.BASE_URL}/search?query={query}",
                            wait_until="domcontentloaded")
            await page.wait_for_timeout(SEARCH_WAIT_MS)

            product_sel = [
                "[data-testid='product-card-name']",
                "[class*='ProductName']",
                "[class*='product-name']",
                "[class*='name']",
                "h3", "h4",
            ]
            names = []
            for sel in product_sel:
                try:
                    elements = await page.locator(sel).all()
                    for el in elements:
                        txt = (await el.inner_text()).strip()
                        if txt and len(txt) > 3:
                            names.append(txt)
                except Exception:
                    pass
            return list(set(names))

        except Exception as e:
            log.error(f"Zepto search_brand({brand}): {e}")
            return []

    async def run_for_pincode(self, pin_code: str) -> dict:
        result = {s["sku"]: {"available": False, "product_name_found": None, "error": None}
                  for s in SKUS}
        page = await self._get_page()
        try:
            ok = await self.set_location(page, pin_code)
            if not ok:
                for s in SKUS:
                    result[s["sku"]]["error"] = "location_failed"
                return result

            for brand, brand_queries in BRAND_SEARCH_TERMS.items():
                brand_skus = [s for s in SKUS if s["brand"] == brand]
                if not brand_skus:
                    continue
                found_names: list[str] = []
                for q in brand_queries:
                    names = await self.search_brand(page, q)
                    found_names.extend(names)
                    if names:
                        break

                for sku in brand_skus:
                    for pname in found_names:
                        if sku_matched(sku, pname):
                            result[sku["sku"]]["available"] = True
                            result[sku["sku"]]["product_name_found"] = pname
                            break

                log.info(f"  Zepto {pin_code} | {brand}: "
                         f"{sum(1 for s in brand_skus if result[s['sku']]['available'])}/"
                         f"{len(brand_skus)} found")

        except Exception as e:
            log.error(f"Zepto run_for_pincode({pin_code}): {e}")
            if SCREENSHOT_ON_ERROR:
                await page.screenshot(path=str(SCREENSHOT_DIR / f"zepto_{pin_code}_err.png"))
        finally:
            await page.close()
        return result


# ─── SWIGGY INSTAMART ─────────────────────────────────────────────────────────

class SwiggyInstamartScraper:
    BASE_URL = "https://www.swiggy.com/instamart"
    NAME = "swiggy"

    def __init__(self, context: BrowserContext, debug: bool = False):
        self.context = context
        self.debug = debug

    async def _get_page(self) -> Page:
        page = await self.context.new_page()
        page.set_default_timeout(PAGE_TIMEOUT_MS)
        return page

    async def set_location(self, page: Page, pin_code: str) -> bool:
        try:
            await page.goto(self.BASE_URL, wait_until="domcontentloaded")
            await page.wait_for_timeout(2000)

            loc_selectors = [
                "span:has-text('Deliver to')",
                "[data-testid='header-address']",
                "[class*='HeaderAddress']",
                "header button",
                "[class*='location']",
            ]
            for sel in loc_selectors:
                try:
                    el = page.locator(sel).first
                    if await el.is_visible(timeout=2000):
                        await el.click()
                        break
                except Exception:
                    pass

            await page.wait_for_timeout(1000)

            input_sel = [
                "input[placeholder*='Search for']",
                "input[placeholder*='Enter your']",
                "input[placeholder*='Search']",
                "input[type='text']",
            ]
            for sel in input_sel:
                try:
                    inp = page.locator(sel).first
                    if await inp.is_visible(timeout=2000):
                        await inp.fill(pin_code)
                        await page.wait_for_timeout(SEARCH_WAIT_MS)
                        break
                except Exception:
                    pass

            sug_sel = [
                "[class*='PlaceSuggestion']",
                "[data-testid*='location']",
                "[role='option']",
                "ul li",
            ]
            for sel in sug_sel:
                try:
                    sug = page.locator(sel).first
                    if await sug.is_visible(timeout=2000):
                        await sug.click()
                        await page.wait_for_timeout(2000)
                        return True
                except Exception:
                    pass

            await page.keyboard.press("Enter")
            await page.wait_for_timeout(2000)
            return True

        except Exception as e:
            log.error(f"Swiggy set_location({pin_code}): {e}")
            if SCREENSHOT_ON_ERROR:
                await page.screenshot(path=str(SCREENSHOT_DIR / f"swiggy_loc_{pin_code}.png"))
            return False

    async def search_brand(self, page: Page, brand: str) -> list[str]:
        try:
            # Swiggy search URL pattern
            query = brand.replace("&", "").replace(" ", "%20")
            await page.goto(
                f"https://www.swiggy.com/instamart/search?custom_back=true&query={query}",
                wait_until="domcontentloaded"
            )
            await page.wait_for_timeout(SEARCH_WAIT_MS)

            product_sel = [
                "[data-testid='item_name']",
                "[class*='ItemName']",
                "[class*='item-name']",
                "[class*='product-name']",
                "h3", "h4",
            ]
            names = []
            for sel in product_sel:
                try:
                    elements = await page.locator(sel).all()
                    for el in elements:
                        txt = (await el.inner_text()).strip()
                        if txt and len(txt) > 3:
                            names.append(txt)
                except Exception:
                    pass
            return list(set(names))

        except Exception as e:
            log.error(f"Swiggy search_brand({brand}): {e}")
            return []

    async def run_for_pincode(self, pin_code: str) -> dict:
        result = {s["sku"]: {"available": False, "product_name_found": None, "error": None}
                  for s in SKUS}
        page = await self._get_page()
        try:
            ok = await self.set_location(page, pin_code)
            if not ok:
                for s in SKUS:
                    result[s["sku"]]["error"] = "location_failed"
                return result

            for brand, brand_queries in BRAND_SEARCH_TERMS.items():
                brand_skus = [s for s in SKUS if s["brand"] == brand]
                if not brand_skus:
                    continue
                found_names: list[str] = []
                for q in brand_queries:
                    names = await self.search_brand(page, q)
                    found_names.extend(names)
                    if names:
                        break

                for sku in brand_skus:
                    for pname in found_names:
                        if sku_matched(sku, pname):
                            result[sku["sku"]]["available"] = True
                            result[sku["sku"]]["product_name_found"] = pname
                            break

                log.info(f"  Swiggy {pin_code} | {brand}: "
                         f"{sum(1 for s in brand_skus if result[s['sku']]['available'])}/"
                         f"{len(brand_skus)} found")

        except Exception as e:
            log.error(f"Swiggy run_for_pincode({pin_code}): {e}")
            if SCREENSHOT_ON_ERROR:
                await page.screenshot(path=str(SCREENSHOT_DIR / f"swiggy_{pin_code}_err.png"))
        finally:
            await page.close()
        return result


# ─── Orchestrator ─────────────────────────────────────────────────────────────

async def run_platform(scraper_cls, pin_codes: list[str], debug: bool) -> dict:
    """Run one platform across all pin codes, return {pin: {sku: result}}."""
    platform_results = {}
    async with async_playwright() as pw:
        browser = await pw.chromium.launch(
            headless=(not debug),
            slow_mo=SLOW_MO_MS if not debug else 200,
            args=[
                "--no-sandbox",
                "--disable-blink-features=AutomationControlled",
                "--disable-dev-shm-usage",
            ]
        )
        context = await browser.new_context(
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/124.0.0.0 Safari/537.36"
            ),
            viewport={"width": 1280, "height": 800},
            locale="en-IN",
            timezone_id="Asia/Kolkata",
        )
        # Remove webdriver flag
        await context.add_init_script(
            "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
        )

        scraper = scraper_cls(context=context, debug=debug)
        log.info(f"▶  Platform: {scraper.NAME.upper()} | {len(pin_codes)} pin codes")

        for pin in pin_codes:
            log.info(f"  → {pin} ({PIN_CODES[pin]['area']})")
            pin_result = await scraper.run_for_pincode(pin)
            platform_results[pin] = pin_result
            # Small cooldown between pin codes
            await asyncio.sleep(1.5)

        await browser.close()
    return platform_results


async def main(platforms: Optional[list[str]] = None,
               pin_codes: Optional[list[str]] = None,
               debug: bool = False):

    start = datetime.now()
    if platforms is None:
        platforms = ["blinkit", "zepto", "swiggy"]
    if pin_codes is None:
        pin_codes = list(PIN_CODES.keys())

    results = load_results()
    if not results:
        results = init_result_structure()

    PLATFORM_MAP = {
        "blinkit": BlinkitScraper,
        "zepto":   ZeptoScraper,
        "swiggy":  SwiggyInstamartScraper,
    }

    for platform in platforms:
        cls = PLATFORM_MAP.get(platform)
        if cls is None:
            log.warning(f"Unknown platform: {platform}")
            continue
        platform_data = await run_platform(cls, pin_codes, debug)
        for pin, pin_data in platform_data.items():
            results["data"][platform][pin] = pin_data

    elapsed = (datetime.now() - start).total_seconds()
    results["meta"]["last_run"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    results["meta"]["run_duration_s"] = round(elapsed, 1)
    save_results(results)
    log.info(f"✓  Done in {elapsed:.0f}s")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--platform", choices=["blinkit", "zepto", "swiggy"],
                        help="Run only this platform")
    parser.add_argument("--pincode", help="Run only this pin code")
    parser.add_argument("--debug", action="store_true",
                        help="Show browser, slow mode")
    args = parser.parse_args()

    platforms = [args.platform] if args.platform else None
    pin_codes = [args.pincode] if args.pincode else None

    asyncio.run(main(platforms=platforms, pin_codes=pin_codes, debug=args.debug))
