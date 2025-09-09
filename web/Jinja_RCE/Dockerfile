FROM python:3.12-slim

WORKDIR /app
RUN adduser --disabled-password --gecos '' ctf && chown -R ctf /app
COPY app.py /app/
RUN pip install --no-cache-dir flask==3.0.3

USER ctf
EXPOSE 5000
ENV FLAG=CHALL{jinja_mailer_rce}
CMD ["python", "app.py"]
