FROM python:3-slim

# Install dependencies
COPY requirements.txt /tmp/requirements.txt
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc libmariadb-dev && \
	pip3 install --no-cache -r /tmp/requirements.txt && \
    apt-get purge -y gcc && \
    apt-get autoremove -y --purge && \
    apt-get autoclean && \
    rm -rf /tmp/requirements.txt /var/log/apt /var/cache/apt/ /var/lib/apt/

# Copy code
COPY . /app/
WORKDIR /app

# Set permission
RUN chown nobody:nogroup -R /app

EXPOSE 8000
USER nobody

CMD gunicorn wsgi:app -b 0.0.0.0:8000
