FROM python:3.12.1-slim

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip

WORKDIR /app

COPY requirements requirements

RUN pip install -r requirements/local.txt

COPY . .

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

