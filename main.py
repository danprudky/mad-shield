from mad_shield import *

mad_shield = MadShield("mad_shield/config/agents.yaml", 1)

mad_shield.go("test/alert/sql_injection")
