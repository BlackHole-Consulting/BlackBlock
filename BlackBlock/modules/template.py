## main program base libraries

from colorama import init
from colorama import Fore, Back, Style, Cursor
import resource as res

import requests
import datetime as dt
import time
## eos node libraries


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


from prettytable import PrettyTable
import random

## encryption eos libraries

import BlackBlock.modules.resources.config as conf
from rich.console import Console



console = Console()

def moduleInfo():
	info = {
	'name': 'template',
	'description': 'template module',
	'version': '1.0',
	'category': ''
	}

	return info



def genkeys(options):

	secp_k = generate_eth_key()
	print("Private : "+secp_k.to_hex())
	print("Public : "+secp_k.public_key.to_hex())



## Extend command usage instructions 
def ExtendCommands():
	commands = [
	["genkeys","genkeys"]
	]
	return commands

## Set module options
def moduleOptions():
	options = [
	["account", "set your RHOMB account", "msig"], 
	["pubkey", "set your RHOMB pubkey", ""],
	["filter", "set filter words or event type", "0"],
	["server", "set your RHOMB server ip:port", "http://block.things360.io:8888"]
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
