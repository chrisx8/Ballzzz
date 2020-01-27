FROM python:3-alpine

# Install system packages
RUN apk add --no-cache postgresql-dev mariadb-connector-c-dev && \
    echo 'nameserver 127.0.0.11' > /etc/resolv.conf && \
    echo 'nameserver 1.1.1.1' >> /etc/resolv.conf && \
    echo 'nameserver 8.8.8.8' >> /etc/resolv.conf

# Install project dependencies
COPY requirements.txt /tmp/requirements.txt
RUN apk add --no-cache build-base gcc musl-dev && \
    pip3 install --no-cache -r /tmp/requirements.txt && \
    rm /tmp/requirements.txt && \
    apk del build-base gcc musl-dev 

# Copy code
COPY . /app/
WORKDIR /app

# Set permission
RUN chown nobody:nogroup -R /app

EXPOSE 8000
USER nobody

CMD gunicorn wsgi:app -b 0.0.0.0:8000
