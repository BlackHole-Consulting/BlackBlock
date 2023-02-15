## main program base libraries

from colorama import init
from colorama import Fore, Back, Style, Cursor
import resource as res

import requests
import datetime as dt
import time

import subprocess
import sys
import os, time
import requests
import json
import BlackBlock.modules.resources.config as conf
## Elk
#from BlackBlock.lib.elk import *
pypatch = os.path.realpath(os.path.dirname(__file__))+'/../'

CURRENCY = 'IDB'

URL_API ='http://localhost:8888'

API = URL_API+'/v1/chain/get_info'
API2 = URL_API+'/v1/producer/schedule_protocol_feature_activations'

wallet_password = ''
ACCOUNTS = {'accounts': [{'name': 'eosio.bpay'},
						 {'name': 'eosio.msig'},
						 {'name': 'eosio.names'},
						 {'name': 'eosio.ram'},
						 {'name': 'eosio.ramfee'},
						 {'name': 'eosio.saving'},
						 {'name': 'eosio.stake'},
						 {'name': 'eosio.token'},
						 {'name': 'eosio.vpay'},
						 {'name': 'eosio.rex'}
]}

config = []
old_config = []
def moduleInfo():
	info = {
	'name': 'setup',
	'description': 'setup module',
	'version': '1.0',
	'category': ''
	}

	return info



def save_to_file():
	global old_config, config
	content = conf.cli.moduleOptions
	try:
		with open(os.path.expanduser('~')+'/.BlackBlock/blackblock-node/config.json', 'w') as writer:
			#writer.write('wda')
			json.dump(content, writer)
	except Exception as err:
		print('ERROR', err)

def load_profile():
	global config
	config = json.load(open(os.path.expanduser('~')+'/.BlackBlock/blackblock-node/config.json'))

def runcmd(cmd):
	p = os.popen(cmd)
	response = p.read().strip()
	return response

def check_node():
	try:
		response = requests.get(url=API)
		response = response.content
		ret = response.decode('utf-8')
		ret = json.loads(ret)
		print('ChainId', ret["chain_id"])
		return True
	except:
		return False

def protocol_features_to_activate():
	data = {"protocol_features_to_activate": ["0ec7e080177b2c02b278d5088611686b49d739925a92d9bfcacd7fc6b74053bd"]}
	headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
	response = requests.post(API2, data=json.dumps(data), headers=headers)
	ret = response.content.decode('utf-8')
	ret = json.loads(ret)
	print(ret)

def download_resources():
	print('Downloading... eosio.contracts')
	runcmd('git clone --quiet https://github.com/EOSIO/eosio.contracts.git ~/eosio.contracts')

	runcmd('cd ~/eosio.contracts;git checkout release/1.9.x;./build.sh -y')

def create_wallet(profile):

	response = runcmd('cleos wallet create -n default --to-console')
	response = response.split('\n')
	for resp in response:
		#print('caca', resp)
		if '"' in resp:
			return resp
	return None

def cleanwallet():
	runcmd('cleos wallet stop')
	runcmd('rm -rf '+os.path.expanduser('~')+'/eosio-wallet')
	#runcmd('cd ~/.BlackBlock/blackblock-node/;rm *.sh')
	runcmd('cd '+os.path.expanduser('~')+'/.BlackBlock/blackblock-node/;pwd')
	runcmd('rm -r '+os.path.expanduser('~')+'/.BlackBlock')
	runcmd('mkdir '+os.path.expanduser('~')+'/.BlackBlock')
	runcmd('mkdir '+os.path.expanduser('~')+'/.BlackBlock/blackblock-node')
	#runcmd('touch '+os.path.expanduser('~')+'/.BlackBlock/blackblock genesis_run.json')

	#runcmd('rm default.wallet')
	#runcmd('rm accounts')
	#runcmd('rm keypairs')

def import_wallet(pkey):
	return runcmd('cleos wallet import --private-key '+pkey)


def create_account(acc, pubkey):

	print("Creating ", acc)
	return runcmd('cleos create account eosio '+acc+' '+pubkey)


def install_contract():

	print('#Install the eosio.token contract')
	runcmd('cleos set contract eosio.token ~/eosio.contracts/build/contracts/eosio.token/')

	print('#Set the eosio.msig contract')
	runcmd('cleos set contract eosio.msig ~/eosio.contracts/build/contracts/eosio.msig/')

	COINS = '[ "eosio", "5000000000.0000 '+CURRENCY+'" ]'
	COINS2 = '[ "eosio", "5000000000.0000 '+CURRENCY+'", "memo" ]'
	print('#Create and allocate the SYS currency , CON')
	
	runcmd("cleos push action eosio.token create '"+str(COINS)+"' -p eosio.token@active")
	runcmd("cleos push action eosio.token issue '''''"+str(COINS2)+"''''' -p eosio@active")
	protocol_features_to_activate()


def genkeys():
	

	response = runcmd('cleos create key --to-console')
	response = response.split('\n')
	print('KEYS',response)
	for resp in response:
		if 'Private' in resp:
			priv_key = resp.replace('Private key: ','')
		if 'Public' in resp:
			pub_key = resp.replace('Public key: ','')
	return priv_key, pub_key




def get_accounts():

	for acc in ACCOUNTS["accounts"]:
		priv, pub = genkeys()
		acc["pub"] = pub
		acc["priv"] = priv
		print(import_wallet(priv))

def set_accounts():

	for acc in ACCOUNTS["accounts"]:
		create_account(acc["name"], acc["pub"])


def unlock_wallet(password):
	runcmd('cleos wallet unlock --password '+password)
	



def make_node(profile, pubkey, privatekey):

	with open(pypatch+'resources/genesis.json', 'r') as reader:
		# Read & print the entire file
		genesis = reader.read()
	runcmd('cp '+pypatch+'resources/genesis.json '+os.path.expanduser('~')+'/.BlackBlock/blackblock-node/genesis_run.json')
	with open(os.path.expanduser('~')+'/.BlackBlock/blackblock-node/genesis_run.json', 'w') as writer:
		writer.write(genesis.replace('PUB_KEY',pubkey))

	with open(pypatch+'resources/node_start.sh', 'r') as reader:
		# Read & print the entire file
		genesis_sh = reader.read()
	runcmd('cp '+pypatch+'resources/node_start.sh '+os.path.expanduser('~')+'/.BlackBlock/blackblock-node/node_start.sh')
	with open(os.path.expanduser('~')+'/.BlackBlock/blackblock-node/node_start.sh', 'w') as writer:
		writer.write(genesis_sh.replace('PUB_KEY',pubkey).replace('PRIVATE_KEY',privatekey))

	runcmd('cp '+pypatch+'resources/stop.sh '+os.path.expanduser('~')+'/.BlackBlock/blackblock-node/stop.sh')
	runcmd('cp '+pypatch+'resources/clean.sh '+os.path.expanduser('~')+'/.BlackBlock/blackblock-node/clean.sh')
	#runcmd('cp resources/node_start.py '+os.path.expanduser('~')+'/.BlackBlock/blackblock-node/node_start.py')


def install_node(options):
	global wallet_password, ACCOUNTS
	#cleanwallet()
	profile = 'node'
	#if not os.path.exists(os.path.expanduser('~')+'/.BlackBlock/blackblock'):
	#	os.makedirs(os.path.expanduser('~')+'/.BlackBlock/blackblock')
	if not os.path.exists(os.path.expanduser('~')+'/.BlackBlock/blackblock-node'):
		os.makedirs(os.path.expanduser('~')+'/.BlackBlock/blackblock-node')
	try:
		wallet_password = create_wallet(profile)
		if not wallet_password == None:
			print('wallet_password', wallet_password)
			with open(os.path.expanduser('~')+'/.BlackBlock/blackblock-node/password', 'w') as writer:
				#json.dump(wallet_password, writer)
				writer.write(wallet_password.replace('"', ''))
	except:
		pass
	runcmd('mkdir '+os.path.expanduser('~')+'/.BlackBlock/blackblock-node')
	#print('GET ACCOUNTS')
	#get_accounts()
	priv, pub = genkeys()
	print(import_wallet(priv))
	print('MAKE NODE ')
	ACCOUNTS = {}
	ACCOUNTS['priv'] = priv
	ACCOUNTS['pub'] = pub
	make_node(profile, pub, priv)

	with open(os.path.expanduser('~')+'/.BlackBlock/blackblock-node/accounts.json', 'w') as writer:
		#writer.write('wda')
		json.dump(ACCOUNTS, writer)



	node_state = check_node()

	print(node_state)

	if node_state == False:
		
		runcmd('cd '+os.path.expanduser('~')+'/.BlackBlock/blackblock-node/; chmod +x *.sh')
		os.system('cd '+os.path.expanduser('~')+'/.BlackBlock/blackblock-node/; ./node_start.sh')
		print('Running Node')
		time.sleep(3)



	print(check_node())
	#unlock_wallet(wallet_password)
	print('SET ACCOUNTS')
	#set_accounts()
	time.sleep(3)
	create_account('ctx3', pub)
	#install_contract()
	save_to_file()

def status(options):

	print('Status', check_node())


def unlock(options):
	unlock_wallet(options[0])

def start(options):
	os.system('cd '+os.path.expanduser('~')+'/.BlackBlock/blackblock-node/; ./node_start.sh')

def stop(options):
	os.system('cd '+os.path.expanduser('~')+'/.BlackBlock/blackblock-node/; ./stop.sh')
def restart(options):
	stop('a')
	time.sleep(3)
	start('a')
def clean(options):
	cleanwallet()

def save_config(options):
	if conf.profile == '':
		print('Need select profile to save')
		return
	save_to_file()

def load(options):
	if conf.profile == '':
		print('Need select profile to load')
		return
	PROFILES = get_profiles()
	config = json.load(open(os.path.expanduser('~')+'/.BlackBlock/blackblock-node/config.json'))
	conf.cli.moduleOptions = config

## Extend command usage instructions 
def ExtendCommands():
	commands = [
	["start","start blockchain"],
	["stop","stop blockchain"],
	["restart","restart blockchain"],
	["install_node","install node blockchain"],
	#["install_genesis","install genesis and contracts"],
	["status","status node"],
	["unlock","unlock walletpassword"],
	["download_resources","download and build contracts"],
	["clean","clean"]
	#["load","load config"],
	#["save_config","save config"]
	

	]
	return commands

def get_profiles():
    return os.listdir(os.path.expanduser('~')+'/.BlackBlock/blackblock')
 

## Set module options
def moduleOptions():
	options = [
	#["profile", "set your node name", "nodo"],
	#["ip", "set your node name", ""],
	#["http_port", "set your node name", ""],
	#["p2p_port", "set your node name", ""]
	]
	
	return options

## Define core params
def save(cli, moduleOptions):
	global config
	conf.cli = cli #cli instance
	try:
		conf.profile = moduleOptions[0][2]
		#if conf.profile != moduleOptions[0][2]:
		#	conf.profile = moduleOptions[0][2]
		#	load_profile()
		#else:
		#	conf.profile = moduleOptions[0][2]
		#try:
		#	config['profile'] = conf.profile
		#except:
		#	pass
		#save_to_file()
	except Exception as err:
		print('error', err)
		pass
	#conf.server  = moduleOptions[3][2]
	#file1 = open('bash/default.wallet', 'r')
	#Lines = file1.readlines()
	 
	#for line in Lines:
	#	if '"' in line:
	#		conf.password = line.replace('"', '')
	print('RUN')
	#print("\033[1;34m"+"[*]"+"\033[0m"+conf.channels)
