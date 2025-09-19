FROM python:3.10-slim

WORKDIR /app

# Copy files
COPY app.py /app
COPY templates/ /app/templates/
COPY entrypoint.sh /entrypoint.sh

# Install dependencies
RUN pip install flask lxml && chmod +x /entrypoint.sh

EXPOSE 5000
ENTRYPOINT ["/entrypoint.sh"]
