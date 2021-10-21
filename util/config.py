""" IP and PORT for the directory service """
DIR_IP = "192.168.1.204"
DIR_PORT = "7777"

""" Load Balancer server update frequency from directory service """
PERIODIC_UPDATE = 60 # Seconds

""" Game and Api-server heartbeat frequency """
HEARTBEAT_FREQUENCY = 3 # Seconds

""" Load balancer drops a server if its been longer then TIMEOUT since last usage update """
TIMEOUT = 10 # Seconds