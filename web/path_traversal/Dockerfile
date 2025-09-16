FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Create directory with sample files
RUN mkdir files && echo "Hello CTF Player!" > files/hello.txt && echo "Try harder..." > files/note.txt

COPY app.py .
COPY templates ./templates

# flag will be written dynamically by app.py using env GZCTF_FLAG
EXPOSE 8000

CMD ["python", "app.py"]
