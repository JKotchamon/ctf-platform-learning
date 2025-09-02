# entrypoint.sh
#!/bin/sh
set -e

# GZ::CTF will set this per-instance. Provide a safe fallback for local dev.
FLAG="${GZCTF_FLAG:-CTF{dev_static_fallback}}"

# Inject the flag into About page (hidden comment placeholder)
# We replace the token %%FLAG%% in about.html with the real flag.
sed -i "s|%%FLAG%%|$FLAG|g" /usr/share/nginx/html/about.html

# nothing else to do here; nginx will be started by CMD
