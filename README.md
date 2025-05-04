# MAD-Shield

TODO: Doplnit abstract

### Run DoS attack on docker containers

1. Run containers
```
cd test/dos
docker compose up -d --build
```

2. Connect to containers from different terminals
```
docker exec -it dos_defender /bin/bash
```

```
docker exec -it dos_attacker /bin/bash
```

#### Run on dos_defender
3. Update suricatas rules
```
suricata-update
```

3. Update defender's python
```
apt-get update
add-apt-repository ppa:deadsnakes/ppa
apt install python3.12
apt-get install wget
wget https://bootstrap.pypa.io/get-pip.py
python3.12 get-pip.py
```

4. Install MAD-Shield requirements
```
python3.12 -m pip install --upgrade pip
python3.12 -m pip install -r /usr/local/bin/mad-shield/requirements.txt
```

You will probably have to download another libraries for MAD-Shield to work with, base on type of attacks you expected.

5. Run services in different terminals
```
python3.12 /usr/local/bin/mad-shield/run.py --debug --max-debate-rounds 4
```

```
suricata -c /etc/suricata/suricata.yaml -i eth0
```

#### Run on dos_defender
6. Run attack
```
python3 /usr/local/bin/dos_attack.py
```