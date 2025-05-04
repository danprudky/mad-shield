FROM ubuntu:22.04

RUN apt-get update && \
    apt-get install -y software-properties-common && \
    add-apt-repository ppa:oisf/suricata-stable -y && \
    apt-get update && \
    apt-get install -y suricata && \
    rm -rf /var/lib/apt/lists/*

COPY mad-shield/test/dos/defender/suricata.yaml /etc/suricata/suricata.yaml
COPY mad-shield/test/dos/defender/detect-dos.rules /etc/suricata/rules/detect-dos.rules

COPY mad-shield/run.py /usr/local/bin/mad-shield/
COPY mad-shield/requirements.txt /usr/local/bin/mad-shield/
COPY mad-shield/.env /usr/local/bin/mad-shield/
COPY mad-shield/mad_shield /usr/local/bin/mad-shield/mad_shield

CMD ["tail", "-f", "/dev/null"]