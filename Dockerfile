FROM mcr.microsoft.com/playwright/python:v1.44.0-jammy

WORKDIR /app
COPY . .
RUN pip3 install flask playwright

EXPOSE 8080
CMD ["python3", "app.py"]
