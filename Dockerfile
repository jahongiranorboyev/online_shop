FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /code

# netcat va gettext o'rnatiladi
RUN apt-get update && apt-get install -y netcat-openbsd gettext && apt-get clean

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chmod +x /code/entrypoint.sh /code/wait_for_db.sh

ENTRYPOINT ["/code/entrypoint.sh"]
