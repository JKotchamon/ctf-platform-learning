FROM python:3.9-slim

WORKDIR /app
COPY app.py /app/
COPY entrypoint.sh /app/
RUN chmod +x /app/entrypoint.sh

RUN pip install flask

# Expose port 5000
EXPOSE 5000

ENTRYPOINT ["/app/entrypoint.sh"]
