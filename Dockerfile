FROM python:3.12
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
RUN python -m playwright install --with-deps chromium firefox webkit
CMD ["python", "app/app.py"]
