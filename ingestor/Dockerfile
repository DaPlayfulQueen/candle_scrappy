FROM python:3.9-alpine

WORKDIR /app
COPY requirements.txt /app/
COPY ingest.py /app/
COPY crontab.txt /crontab.txt

RUN pip install -r requirements.txt
RUN /usr/bin/crontab /crontab.txt
RUN chmod +x /app/ingest.py

CMD ["crond", "-f", "-d", "8"]
# CMD ["python", "/app/ingest.py"]
