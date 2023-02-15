## main program base libraries

from colorama import init
from colorama import Fore, Back, Style, Cursor
import resource as res

import requests
import datetime as dt
import time
## eos node libraries
import eospy.cleos
import eospy.keys
from eospy.types import Abi, Action
from eospy.utils import parse_key_file

## utils
import pytz
import re
import json
import subprocess
import shlex
import hashlib
import binascii
import unittest
import pickle

## eos node ibraries
from eospy.cleos import Cleos
from prettytable import PrettyTable
import random

## encryption eos libraries
from ecies.utils import generate_eth_key, generate_key
from ecies import encrypt, decrypt
import BlackBlock.modules.resources.config as conf
from rich.console import Console

## Elk
#from BlackBlock.lib.elk import *


console = Console()

def moduleInfo():
	info = {
	'name': 'block',
	'description': 'blockchain module',
	'version': '1.0',
	'category': ''
	}

	return info


def terminal(stdin, return_data=False):

	cmd_list = 'cleos '
	tmp_stdout = str()
	for item in stdin:
		cmd_list += str(item) +' '
	sp = subprocess.Popen(shlex.split(cmd_list.strip()), stdout=subprocess.PIPE)
	while True:
		output = sp.stdout.readline()
		if sp.poll() is not None:
			break
		if output:
			if return_data == True:
				tmp_stdout += output.strip().decode() + '\n'
			else:
				print (output.strip().decode().replace("cleos","Black").replace("eosio","black").replace("EOSIO","BLACK").replace("nodeos","black"))
	rc = sp.poll()
	if return_data == True:
		return tmp_stdout.replace("cleos","Black").replace("eosio","black").replace("EOSIO","BLACK").replace("nodeos","black")


def regxp(dat,exp):
	
	for line in f:
		match = re.search('f\(\s*([^,]+)\s*,\s*([^,]+)\s*\)', line)
	if match:
		return True
	else:
		return False

# Get random node
def randnode():
	lines = open('modules/nodes').read().splitlines()
	myline =random.choice(lines)
	return (myline)


## encrypt data using a ECC public key
def enc_ecc(msg):

	pubKeyHex = conf.ethpubkey
	plaintext = msg
	encrypted = encrypt(pubKeyHex, plaintext.encode())
	return encrypted

## decrypt data using a ECC privatekey
def dec_ecc(msg):
	msgen = msg
	msgen = binascii.unhexlify(d_encode(msgen))
	return decrypt(conf.ethprivkey, msgen).decode()


def serialize(data):
		return pickle.dumps(data)


def deserialize(data):
		return pickle.loads(data)


def d_encode(str, code='utf-8'):
		return str.encode(code)


def d_decode(bytes, code='utf-8'):
		return bytes.decode(code)


def test_all(asd):

	try:
		console.log('[bold green]TEST GENKEYS')
		conf.cli.commandHandler('genkeys')
	except:
		console.log('[bold red]ERROR genkeys')
		pass

	try:
		console.log('[bold green]TEST ENC')
		str_enc = enc(['sacs'])
		str_enc2 = binascii.hexlify(str_enc)
		print(str_enc2)
	except:
		console.log('[bold red]ERROR enc')
		pass

	##ERROR
	try:
		console.log('[bold green]TEST DEC')
		str_dec = dec_ecc(str_enc2)
	except:
		console.log('[bold red]ERROR dec')
		pass
	##

	try:
		console.log('[bold green]TEST CORE')
		conf.cli.commandHandler('core get info')
	except:
		console.log('[bold red]ERROR core get info')
		pass

	try:
		console.log('[bold green]TEST list_devices')
		conf.cli.commandHandler('list_devices 0')
	except:
		console.log('[bold red]ERROR list_devices')
		pass

	try:
		console.log('[bold green]TEST wallet unlock')
		conf.cli.commandHandler('core wallet unlock --password '+conf.password)
	except:
		console.log('[bold red]ERROR wallet unlock')
		pass

	try:
		console.log('[bold green]TEST transfer eosio testacc')
		conf.cli.commandHandler('core transfer eosio testacc "1000.0000 BLACK" ""')
	except:
		console.log('[bold red]ERROR transfer eosio testacc')
		pass

	try:
		console.log('[bold green]TEST get currency balance')
		conf.cli.commandHandler('core get currency balance eosio.token eosio BLACK')
	except:
		console.log('[bold red]ERROR get currency balance')
		pass

	try:
		console.log('[bold green]TEST get table payloads')
		conf.cli.commandHandler('core get table payloads payloads code')
	except:
		console.log('[bold red]ERROR get table payloads')
		pass

	try:
		console.log('[bold green]TEST get table devices')
		conf.cli.commandHandler('core get table devices devices sensors')
	except:
		console.log('[bold red]ERROR get table devices')
		pass

	try:
		console.log('[bold green]TEST get table events')
		conf.cli.commandHandler('core get table events events sensor')
	except:
		console.log('[bold red]ERROR get table events')
		pass

	try:
		console.log('[bold green]TEST get table sensors')
		conf.cli.commandHandler('core get table sensors sensors sensors')
	except:
		console.log('[bold red]ERROR get table sensors')
		pass

	try:
		console.log('[bold green]TEST push action events')
		conf.cli.commandHandler('core push action events upsert ''["eosio","tempnitro" "temperature_sensor"]'' -p eosio@active')
	except:
		console.log('[bold red]ERROR push action events')
		pass

	try:
		console.log('[bold green]TEST push action sensors')
		conf.cli.commandHandler('core push action sensors upsert ''["eosio","tempnitro" "temperature_sensor"]'' -p eosio@active')
	except:
		console.log('[bold red]ERROR push action sensors')
		pass

	try:
		console.log('[bold green]TEST push action devices')
		conf.cli.commandHandler('core push action devices upsert ''["eosio","block.blackrabbit.is","xx","xx","xx","xx","xx","xx","xx","xx","xx"]'' -p eosio@active')
	except:
		console.log('[bold red]ERROR push action devices')
		pass


	try:
		console.log('[bold green]TEST push action payloads')
		conf.cli.commandHandler('core push action payloads upsert ''["eosio","block.blackrabbit.is","xx","xx","xx","xx"]'' -p eosio@active')
	except:
		console.log('[bold red]ERROR push action payloads')
		pass


#	try:
#		console.log('[bold green]TEST get')
#		conf.cli.commandHandler('core')
#	except:
#		console.log('[bold red]ERROR get')
#		pass





def del_char(self, string, indexes):

	return ''.join((char for idx, char in enumerate(string) if idx not in indexes))


def genkeys(options):

	secp_k = generate_eth_key()
	print("Private : "+secp_k.to_hex())
	print("Public : "+secp_k.public_key.to_hex())

def send(options):

	console.log(conf.privkey)
	ce = eospy.cleos.Cleos(url=conf.server)
	addr2 = options[0]
	msg = options[1]
	console.log('[bold red]To: '+str(addr2))
	arguments = {"from": conf.account, "to": addr2, "quantity": '0.0001 BLACK', "memo": msg}
	payload = {"account": "eosio.token", "name": "transfer", "delay_sec": 0, "authorization": [{"actor": conf.account, "permission": "owner"}]}
	data = ce.abi_json_to_bin(payload['account'], payload['name'], arguments)
	payload['data'] = data['binargs']
	trx = {"actions": [payload]}
	trx['expiration'] = str((dt.datetime.utcnow() + dt.timedelta(seconds=60)).replace(tzinfo=pytz.UTC))
	key = eospy.keys.EOSKey(conf.privkey)
	

	try:
		resp = ce.push_transaction(trx, key, broadcast=True)
		print('transaction_id : ', resp['transaction_id'])
		print('status : ', resp['processed']['receipt']['status'])
		print('cpu_usage_us : ', resp['processed']['receipt']['cpu_usage_us'])
		print('net_usage : ', resp['processed']['net_usage'])
		print('from : ', resp["processed"]["action_traces"][0]["act"]["data"]["from"])
		print('to : ', resp["processed"]["action_traces"][0]["act"]["data"]["to"])
	except requests.exceptions.RequestException as e:
		print('ERROR: ', e)
		pass


## Receive data from a eos address, decrypts if the messages are encrypted
def receive(options):
		x = rcv(options, prettyt=True)
		print(x) 

def rcv(options, prettyt=True):
		addr = options[0]
		templist = list()
		x = PrettyTable(["Sensor","Event","Date","Data"])
		ce = Cleos(url=conf.server)
		get_actions = ce.get_actions(addr)
		
		for x1 in get_actions["actions"]:
			try:
				d_memo = x1["action_trace"]["act"]["data"]["memo"]
				d_from = x1["action_trace"]["act"]["data"]["from"]
				if prettyt == False:
					#yield d_memo
					templist.append(d_memo)
				x.add_row([d_from, d_memo,"",""])
			except:
				pass
		if prettyt == True:
			return(x)
		else:
			return templist
	
## List with regexp filter


## send sensors commands
def cmdsensor(options):
	## generate random id
	rndid = random.randint(0, 9999999)
	## encrypt cmd
	datenc = enc_ecc(str(rndid)+"-org-"+options[1])
	## send encrypted cmd + id
	send([options[0], binascii.hexlify(datenc)])
	time.sleep(5)

	while True:
		## wait for sensor response with the id
		for e in rcv([conf.account], False):
			
			try:
				## decrypt data
				decdata = dec_ecc(e)

				if str(rndid)+"-org-" in decdata:
					response = decdata.split(str(rndid)+"-org-")
					console.log('DECODED DATA => ', response[1])
					break
			except rsa.pkcs1.DecryptionError as err:
				pass
			except:
				pass

def list_devices(addr):

	## return sensor program list, temp, co2 ...
	## cleos get table addressbook addressbook people --lower alice --limit 1
	cmd = "get table devices devices sensors --lower "+addr[0]+" --limit 1"
	resp_terminal = terminal(shlex.split(cmd), return_data=True)
	try:
		resp_dict = json.loads(resp_terminal)
		x = PrettyTable()
		x.field_names = ["Key", "Hostname", "arch", "Event_type", "Services", "Data"]
		for table in resp_dict['rows']:
			x.add_row([table['key'], table['hostname'], table['arch'], table['event_type'], table['services'], table['data']])
		print(x)
	except:
		pass

def list_sensors_types(addr):
	## return sensor program list, temp, co2 ...
	## cleos get table addressbook addressbook people --lower alice --limit 1
	cmd = "get table sensors sensors sensor --lower "+addr[0]+" --limit 1"
	terminal(shlex.split(cmd))


def list_event_types(addr):
	
	cmd = "get table evens evens event --lower "+addr[0]+" --limit 1"
	terminal(shlex.split(cmd))


def list_payloads(addr):
	## return sensor program list, temp, co2 ...
	## cleos get table addressbook addressbook people --lower alice --limit 1
	cmd = "get table payloads payloads payload --lower "+addr[0]+" --limit 1"
	terminal(shlex.split(cmd))

		
def upsert_device(options):
	addr=options[0]
	hostname=options[1]
	arch=options[2]
	event_type=options[3]
	services=options[4]
	dat=options[5]
	lt= options[6]
	lat=options[7]
	street=options[8]
	city=options[9]
	state=options[10]
	cmd = "push action devices upsert '[\""+addr+"\",\""+hotname+"\", \""+arch+"\", \""+event_type+"\", \""+services+"\", \""+dat+"\", \""+lt+"\",\""+lat+"\",\""+street+"\",\""+city+"\",\""+state+"\"]' -p "+addr+"@active"
	terminal(shlex.split(cmd))

def upsert_sensor_type(options):
	addr=options[0]
	name=options[1]
	description=options[2]
	cmd = "push action sensors upsert '[\""+name+"\",\""+description+"\"]' -p "+addr+"@active"
	terminal(shlex.split(cmd))


def upsert_payloads(options):
	addr=options[0]
	hotname=options[1]
	arch=options[2]
	event_type=options[3]
	#code=options[4]
	cmd = "push action payloads upsert '[\""+addr+"\",\""+hotname+"\", \""+arch+"\", \""+event_type+"\"]' -p "+addr+"@active"
	terminal(shlex.split(cmd))

def upsert_event_types(options):
	addr=options[0]
	name=options[1]
	description=options[2]
	cmd = "push action events upsert '[\""+name+"\",\""+description+"\"]' -p "+addr+"@active"
	terminal(shlex.split(cmd))

def cron_task(addr,taskcmd, time):
	## set crontab task to the IOT device
	
	return 0


def dec(options):

	cmd_list = ''
	for item in options:
		cmd_list += str(item) +' '
	print(cmd_list.strip())

	decdata = dec_ecc(binascii.hexlify(cmd_list))
	print(decdata.strip())
	#print(enc_ecc(cmd_list.strip()))


def enc(options):

	cmd_list = ''
	for item in options:
		cmd_list += str(item) +' '
	print(cmd_list.strip())

	str_enc = enc_ecc(cmd_list.strip())
	print(str_enc)
	return str_enc


def open_terminal(addr):
	## start terminal console interface
	##loop
	## generate random id
	## encrypt cmd and send encrypted cmd + id
	## wait for sensor response with the id
	## decrypt response
	## show promt and wait for new command
	return true

def core(options):
	terminal(options)


## Extend command usage instructions 
def ExtendCommands():
	commands = [
	["genkeys","genkeys"], 
	["enc","enc 'message'"],
	["dec","dec 'message'"],
	["send", "example (send senderAddress receiverAddress msg)"], 
	["cmdsensor", "example (cmdsensor eosaddress command_line)"], 
	["deploy", "example (deploy eosaddress arquitecture sensor_type)"], 
	["track", "example (track eosaddress task time)"], 
	["services", "example (services eosaddress)"], 
	["receive", "example (receive eosaddress)"],
	["core", "Example (core get info)"],
	["list_devices", "Example (list_devices addr)"],
	["list_payloads", "Example (core get info)"],
	["list_event_types", "Example (list_event_types)"],
	["list_sensor_types", "Example (list_sensor_types)"],
	["upsert_devices", "Example (upsert_devices hostname arch event_type services data longitude latitude street city state)"],
	["upsert_payloads", "Example (upsert_payloads name description service (code_text|file) )"],
	["upsert_sensor_types", "Example (upsert_sensor_types name description)"],
	["upsert_event_types", "Example (upsert_event_types name description)"],
	["test_all", ""]
	]
	return commands

## Set module options
def moduleOptions():
	options = [
	["account", "set your BLACK account", ""], 
	["pubkey", "set your BLACK pubkey", ""],
	["devices", "add or remove BLACK devices", ""],
	["privkey", "set your BLACK privkey", ""],
	["ethpubkey", "set your ETH pubkey", "0x5e371600b5177c801ddcf42bd8c07f02425b300bce5804dda01784cc0110d8a38bb5729da007c9b65e6b5f691f2389a0a685b50f20d70f58c1754306f56b5c30"],
	["ethprivkey", "set your ETH privkey", "0xb373ec676d406f6328a0b443ec847049fe888c29d27dcd85d92838bdff49afba"],
	["channels", "set your address channels, separated by , ", "d3usxm4ch1n4"],
	["filter", "set filter words or event type", "0"],
	["server", "set your BLACK server ip:port", "http://block.blackrabbit.is:8888"]
	]
	return options

## Define core params
def save(cli, moduleOptions):

	conf.cli = cli #cli instance

	conf.account = moduleOptions[0][2]
	conf.pubkey = moduleOptions[1][2]
	conf.devices = moduleOptions[2][2]
	conf.privkey = moduleOptions[3][2]
	#conf.ethpubkey, conf.ethprivkey = rsa.newkeys(512)

	conf.ethpubkey = moduleOptions[4][2]
	conf.ethprivkey = moduleOptions[5][2]

	conf.channels = moduleOptions[6][2]
	conf.s_filter  = moduleOptions[7][2]
	conf.server  = moduleOptions[8][2]
	#file1 = open('bash/default.wallet', 'r')
	#Lines = file1.readlines()
	 
	#for line in Lines:
	#	if '"' in line:
	#		conf.password = line.replace('"', '')
	console.log('RUN')
	#print("\033[1;34m"+"[*]"+"\033[0m"+conf.channels)
