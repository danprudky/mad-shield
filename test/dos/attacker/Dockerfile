FROM python:3.10-slim

RUN apt-get update && \
    apt-get install -y hping3 && \
    rm -rf /var/lib/apt/lists/*

COPY mad-shield/test/dos/attacker/dos_attack.py /usr/local/bin/dos_attack.py

CMD ["tail", "-f", "/dev/null"]
