FROM python:3.9-alpine

WORKDIR /app
COPY requirements.txt /app/
COPY ingest.py /app/

ENV CRON_SCHEDULE "0 * * * *"
RUN pip install -r requirements.txt

CMD crontab -r && echo "$CRON_SCHEDULE /usr/local/bin/python /app/ingest.py > /app/output.txt 2>&1" | crontab - && exec crond -f -d 8
# CMD ["python", "/app/ingest.py"]
