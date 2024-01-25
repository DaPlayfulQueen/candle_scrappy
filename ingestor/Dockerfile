FROM python:3.9-alpine

WORKDIR /app
COPY requirements.txt /app/
COPY ingest.py /app/
COPY cronjob.sh /etc/periodic/hourly/cronjob.sh

RUN pip install -r requirements.txt

RUN chmod +x /etc/periodic/hourly/cronjob.sh
RUN chmod +x /app/ingest.py

CMD ["crond", "-f", "-d", "8"]
# CMD ["python", "/app/ingest.py"]
