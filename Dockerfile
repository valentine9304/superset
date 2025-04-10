FROM python:3.11-slim

WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8000

CMD ["sh", "-c", "alembic upgrade head && python migrate_data.py && gunicorn main:app --bind 0.0.0.0:8000"]
