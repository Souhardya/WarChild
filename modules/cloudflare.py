#!/usr/bin/env python3
from __future__ import print_function


import argparse
import sys
import socket
import binascii
import datetime
import socks
import requests
import colorama
from colorama import Fore, Back, Style
from bs4 import BeautifulSoup
import re 

colorama.init(Style.BRIGHT)

# Author : Souhardya Sardar , Drastic and Morty
# Greets : Binary Sec 


class DNSDumpsterAPI(object):

    

    def __init__(self, verbose=False):
        self.verbose = verbose

    def display_message(self, s):
        if self.verbose:
            print('[verbose] %s' % s)


    def retrieve_results(self, table):
        res = []
        trs = table.findAll('tr')
        for tr in trs:
            tds = tr.findAll('td')
            pattern_ip = r'([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3})'
            ip = re.findall(pattern_ip, tds[1].text)[0]
            domain = tds[0].text.replace('\n', '')

            additional_info = tds[2].text
            country = tds[2].find('span', attrs={}).text
            autonomous_system = additional_info.split(' ')[0]
            provider = ' '.join(additional_info.split(' ')[1:])
            provider = provider.replace(country, '')
            data = {'domain': domain, 'ip': ip, 'as': autonomous_system, 'provider': provider, 'country': country}
            res.append(data)
        return res

    def retrieve_txt_record(self, table):
        res = []
        for td in table.findAll('td'):
            res.append(td.text)
        return res


    def search(self, domain):
        dnsdumpster_url = 'https://dnsdumpster.com/'
        s = requests.session()

        req = s.get(dnsdumpster_url)
        soup = BeautifulSoup(req.content, 'html.parser')
        csrf_middleware = soup.findAll('input', attrs={'name': 'csrfmiddlewaretoken'})[0]['value']
        self.display_message('Retrieved token: %s' % csrf_middleware)

        cookies = {'csrftoken': csrf_middleware}
        headers = {'Referer': dnsdumpster_url}
        data = {'csrfmiddlewaretoken': csrf_middleware, 'targetip': domain}
        req = s.post(dnsdumpster_url, cookies=cookies, data=data, headers=headers)

        if req.status_code != 200:
            print(
                u"Unexpected status code from {url}: {code}".format(
                    url=dnsdumpster_url, code=req.status_code),
                file=sys.stderr,
            )
            return []

        if 'error' in req.content.decode('utf-8'):
            print("There was an error getting results", file=sys.stderr)
            return []

        soup = BeautifulSoup(req.content, 'html.parser')
        tables = soup.findAll('table')

        res = {}
        res['domain'] = domain
        res['dns_records'] = {}
        res['dns_records']['dns'] = self.retrieve_results(tables[0])
        res['dns_records']['mx'] = self.retrieve_results(tables[1])
        res['dns_records']['txt'] = self.retrieve_txt_record(tables[2])
        res['dns_records']['host'] = self.retrieve_results(tables[3])
        return res

def print_out(data):
	datetimestr = str(datetime.datetime.strftime(datetime.datetime.now(), '%H:%M:%S'))
	print(Style.NORMAL+"["+datetimestr+"] "+data+Style.RESET_ALL)

def ip_in_subnetwork(ip_address, subnetwork):

    (ip_integer, version1) = ip_to_integer(ip_address)
    (ip_lower, ip_upper, version2) = subnetwork_to_ip_range(subnetwork)
 
    if version1 != version2:
        raise ValueError("incompatible IP versions")
 
    return (ip_lower <= ip_integer <= ip_upper)
 
 
def ip_to_integer(ip_address):

    
    for version in (socket.AF_INET, socket.AF_INET6):
 
        try:
            ip_hex = socket.inet_pton(version, ip_address)
            ip_integer = int(binascii.hexlify(ip_hex), 16)
 
            return (ip_integer, 4 if version == socket.AF_INET else 6)
        except:
            pass
 
    raise ValueError("invalid IP address")
 
 
def subnetwork_to_ip_range(subnetwork):

    try:
        fragments = subnetwork.split('/')
        network_prefix = fragments[0]
        netmask_len = int(fragments[1])
 
        
        for version in (socket.AF_INET, socket.AF_INET6):
 
            ip_len = 32 if version == socket.AF_INET else 128
 
            try:
                suffix_mask = (1 << (ip_len - netmask_len)) - 1
                netmask = ((1 << ip_len) - 1) - suffix_mask
                ip_hex = socket.inet_pton(version, network_prefix)
                ip_lower = int(binascii.hexlify(ip_hex), 16) & netmask
                ip_upper = ip_lower + suffix_mask
 
                return (ip_lower,
                        ip_upper,
                        4 if version == socket.AF_INET else 6)
            except:
                pass
    except:
        pass
 
    raise ValueError("invalid subnetwork")
	
def dnsdumpster(target):
	print_out (Fore.CYAN + "Testing for misconfigured DNS using dnsdumpster...")

	res = DNSDumpsterAPI(False).search(target)

	if res['dns_records']['host']:
		for entry in res['dns_records']['host']:
			provider = str(entry['provider'])
			if "CloudFlare" not in provider:
				print_out(Style.BRIGHT+Fore.WHITE+"[FOUND:HOST] "+Fore.GREEN+"{domain} {ip} {as} {provider} {country}".format(**entry))
	
	if res['dns_records']['dns']:	
		for entry in res['dns_records']['dns']:
			provider = str(entry['provider'])
			if "CloudFlare" not in provider:
				print_out(Style.BRIGHT+Fore.WHITE+"[FOUND:DNS] "+Fore.GREEN+"{domain} {ip} {as} {provider} {country}".format(**entry))
		
	if res['dns_records']['mx']:	
		for entry in res['dns_records']['mx']:
			provider = str(entry['provider'])
			if "CloudFlare" not in provider:
				print_out(Style.BRIGHT+Fore.WHITE+"[FOUND:MX] "+Fore.GREEN+"{ip} {as} {provider} {domain}".format(**entry))

	
def init(target):
	print_out (Fore.CYAN + "Fetching initial information from: "+args.target+"...")

	try:
		ip = socket.gethostbyname(args.target)
	except NetworkException as net_exc:
		print ("error parsing stream", net_exc)
		sys.exit(0)

	print_out(Fore.CYAN + "Server IP: "+ip)
	print_out(Fore.CYAN + "Testing if "+args.target+" is on the Cloudflare network...")

	ifIpIsWithin = inCloudFlare(ip)
					
	if ifIpIsWithin:
		print_out (Style.BRIGHT+Fore.GREEN+ args.target+" is part of the Cloudflare network!")
	else:
		print_out (Fore.RED + args.target+" is not part of the Cloudflare network, quitting...")
		sys.exit(0)
		
		
def inCloudFlare(ip):
	with open('cloudip.txt') as f:
		for line in f:
			isInNetwork = ip_in_subnetwork(ip,line)
			if isInNetwork:
				return True
			else:
				
				continue
		return False
		


logo = """\

\033[92m\033[1m d8888888888888888888888888888    888 .d88888b. 888b    888      \033[92m\033[1m
\033[93m\033[1m      d88888888           888    888    888d88P" "Y88b8888b   888\033[91m\033[1m
\033[91m\033[1m     d88P888888           888    888    888888     88888888b  888\033[92m\033[1m 
\033[92m\033[1m    d88P 8888888888       888    8888888888888     888888Y88b 888\033[94m\033[1m
\033[92m\033[1m   d88P  888888           888    888    888888     888888 Y88b888\033[92m\033[1m 
\033[93m\033[1m  d88P   888888           888    888    888888     888888  Y88888\033[94m\033[1m
\033[93m\033[1m d8888888888888           888    888    888Y88b. .d88P888   Y8888\033[95m\033[1m
\033[94m\033[1md88P     8888888888888    888    888    888 "Y88888P" 888    Y888\033[92m\033[1m
                                                                  
                      
                       \033[92m\033[1mYour IP belongs to us :)\033[94m\033[1m
    \033[92m\033{1mSpecial thanks to Binary Sec Members for the concept specially Drastic and Morty\033[92m\033[1m
"""                 

print(Fore.GREEN+Style.BRIGHT+logo+Fore.RESET)
datetimestr = str(datetime.datetime.strftime(datetime.datetime.now(), '%d/%m/%Y %H:%M:%S'))
print_out("Initializing Aethon - the date/time is: "+datetimestr)

parser = argparse.ArgumentParser()
parser.add_argument("--target", help="target url of website", type=str)
parser.set_defaults(tor=False)

args = parser.parse_args()


try:
    # Initialize CloudFaile
	init(args.target)
		
	# Scan DNSdumpster.com
	dnsdumpster(args.target)

	
except KeyboardInterrupt:
    sys.exit(0)
