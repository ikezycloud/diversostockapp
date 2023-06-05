FROM python:latest

WORKDIR /diverso-stock-app

COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

WORKDIR /diverso-stock-app/shares_broker

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]