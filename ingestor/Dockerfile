ARG CRON_SCHEDULE="0 * * * *"

FROM python:3.9-alpine

WORKDIR /app
COPY requirements.txt /app/
COPY ingest.py /app/

RUN pip install -r requirements.txt

# Set the cron schedule using the build argument
RUN echo "${CRON_SCHEDULE} /usr/local/bin/python /app/ingest.py > /app/output.txt 2>&1" | crontab -

CMD ["crond", "-f", "-d", "8"]
# CMD ["python", "/app/ingest.py"]
