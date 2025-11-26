FROM python:3.12.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN poetry run python manage.py makemigrations
RUN poetry run python manage.py migrate
RUN poetry run python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["uvicorn", "app.asgi:application", "--host", "0.0.0.0", "--port", "8000"]
