FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends gcc libpq-dev && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p uploads/avatars uploads/logos uploads/products

EXPOSE 8000

CMD ["gunicorn", "run:app", "--bind", "0.0.0.0:8000", "--log-file", "-"]
