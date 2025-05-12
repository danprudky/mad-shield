# MAD-Shield
There are several articles in which LLMs are used in multi-agent systems for problem-solving
and have proven themselves in their areas of application. However, no attempt has yet been
made to use a multi-agent system based on LLM agents in the field of cybernetics. Our
system, called MAD-Shield, is based on a centralized multi-agent debate, where participants
represent different parts of the system and, through debate, try to find consensus in the
form of a set of feasible commands. The commands are then executed in the system,
which should lead to a more stable position in the network and minimize vulnerability to
current events. During testing of the system in an emulated environment, MAD-Shield
first prepared a set of defensive commands during the debate, then executed them, but did
not meet our expectations and was unable to stop the attack that was taking place on the
server. The thesis therefore analyzes and proposes solutions that could minimize problems
and bring the system to a functional state.

This system was developed as part of my thesis at Brno University of Technology, Faculty of Information Technology, in 2025.

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