FROM python:3.9-alpine

WORKDIR /app
COPY requirements.txt /app/
COPY etl.py /app/

ENV CRON_SCHEDULE "8 * * * *"
RUN pip install -r requirements.txt

CMD crontab -r && echo "$CRON_SCHEDULE /usr/local/bin/python /app/etl.py" | crontab - && exec crond -f -d 8
# CMD ["python", "/app/etl.py"]
