FROM python:latest

WORKDIR /diverso-stock-app

# Optional: Install SQLite
RUN apt-get update && \
    apt-get install -y sqlite3 libsqlite3-dev

COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

WORKDIR /diverso-stock-app/shares_broker

# Optional: Copy SQLite database file
COPY db.sqlite3 /diverso-stock-app/shares_broker/

# Migrate the database
RUN python manage.py makemigrations
RUN python manage.py migrate

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]