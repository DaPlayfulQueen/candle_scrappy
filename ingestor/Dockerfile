FROM python:3.9-alpine
WORKDIR /app
COPY requirements.txt /app/
COPY ingest.py /app/
RUN pip install -r requirements.txt
RUN "0 * * * * /usr/local/bin/python /app/ingeste.py" > /etc/crontabs/root
RUN chmod +x /app/ingeste.py
CMD ["crond", "-f", "-d", "8"]