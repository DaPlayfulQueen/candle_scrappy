echo "0 * * * * /usr/local/bin/python /app/ingest.py" > /etc/crontabs/root && \
    cat /etc/crontabs/root
