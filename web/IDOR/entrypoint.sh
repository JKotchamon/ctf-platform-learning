#!/bin/sh
# Ensure GZCTF_FLAG is always passed into the app
if [ -z "$GZCTF_FLAG" ]; then
  export GZCTF_FLAG="CTF{DUMMY_FLAG}"
fi

exec python app.py
