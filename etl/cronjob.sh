echo "15 * * * * /usr/local/bin/python /app/etl.py" > /etc/crontabs/root && \
    cat /etc/crontabs/root
