FROM ubuntu:22.04

# 1) Nainstalujeme Suricatu a závislosti
RUN apt-get update && \
    apt-get install -y software-properties-common && \
    add-apt-repository ppa:oisf/suricata-stable -y && \
    apt-get update && \
    apt-get install -y suricata && \
    rm -rf /var/lib/apt/lists/*

# 2) Zkopírujeme konfigurační soubory
COPY suricata.yaml /etc/suricata/suricata.yaml
COPY detect-dos.rules /etc/suricata/rules/detect-dos.rules

CMD ["tail", "-f", "/dev/null"]
