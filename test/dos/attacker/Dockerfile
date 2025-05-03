FROM python:3.10-slim

# 1) Nainstalujeme hping3
RUN apt-get update && \
    apt-get install -y hping3 && \
    rm -rf /var/lib/apt/lists/*

# 2) Zkopírujeme skript
COPY dos_attack.py /usr/local/bin/dos_attack.py

CMD ["tail", "-f", "/dev/null"]
