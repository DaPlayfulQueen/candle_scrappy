FROM python:3.9-alpine

WORKDIR /app
COPY requirements.txt /app/
COPY ingest.py /app/

# Set the default cron schedule during runtime
ENV CRON_SCHEDULE "0 * * * *"

RUN pip install -r requirements.txt

# Set the cron schedule using the environment variable
CMD sh -c 'echo "$CRON_SCHEDULE /usr/local/bin/python /app/ingest.py > /app/output.txt 2>&1" | crontab - && crond -f -d 8'

# CMD ["python", "/app/ingest.py"]
