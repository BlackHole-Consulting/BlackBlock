# BLACKBLOCK CORE

### IOT BLOCKCHAIN CONSOLE


## About

BLACKBLOCK IOT BLOCK, allow to manage BLACKBLOCK IOT devices with blockchain communications using the blockchain transactions as a communication mechanism to interactive and aployment devices and monitorize the events in the network, encrypted with ECC keys .


## Install

```Bash

pip3 install BlackBlock

BlackBlock

```
![image](https://user-images.githubusercontent.com/60758685/218946524-4952865e-cdaf-4c03-b1d8-0721d24d8e2b.png)

## Deploy your node

```Bash

use setup 

install_node

back

```

## Usage 

[![asciicast](https://asciinema.org/a/sz5aGbAc0gJ9bPZ5bLcCbdMAo.svg)](https://asciinema.org/a/sz5aGbAc0gJ9bPZ5bLcCbdMAo)

```Python

use block

BlackBlock $> use block
BlackBlock/block $> core get info
[07:09:49] RUN                                                                                                                                                                               block.py:533
{
"server_version": "025df16c",
"chain_id": "4d490b4f882ef5fb562f53b06478ad1a4b93240eeb708d015053ca83594b3ab0",
"head_block_num": 49651,
"last_irreversible_block_num": 49650,
"last_irreversible_block_id": "0000c1f2c603c825876453f0ca25a36406e517b805a2a2dc142c8c7db42ab8d4",
"head_block_id": "0000c1f370ef3a860080a6360f02029eee6d8ad37e3b28a86e60488ad9aaa198",
"head_block_time": "2023-02-15T01:58:17.500",
"head_block_producer": "black",
"virtual_block_cpu_limit": 100000000,
"virtual_block_net_limit": 1048576000,
"block_cpu_limit": 100000,
"block_net_limit": 1048576,
"server_version_string": "v2.2.0-rc1",
"fork_db_head_block_num": 49651,
"fork_db_head_block_id": "0000c1f370ef3a860080a6360f02029eee6d8ad37e3b28a86e60488ad9aaa198",
"server_full_version_string": "v2.2.0-rc1-025df16c15e08bca17640f93292fdd2c0ffa04f4",
"last_irreversible_block_time": "2023-02-15T01:58:17.000",
"first_block_num": 1
}
BlackBlock/block $> 


options

BlackBlock/block $> options

 Options for module 'block':
	account - set your BLACK account ==> [NOT SET]
	pubkey - set your BLACK pubkey ==> [NOT SET]
	devices - add or remove BLACK devices ==> [NOT SET]
	privkey - set your BLACK privkey ==> [NOT SET]
	ethpubkey - set your ETH pubkey ==> '0x5e371600b5177c801ddcf42bd8c07f02425b300bce5804dda01784cc0110d8a38bb5729da007c9b65e6b5f691f2389a0a685b50f20d70f58c1754306f56b5c30'
	ethprivkey - set your ETH privkey ==> '0xb373ec676d406f6328a0b443ec847049fe888c29d27dcd85d92838bdff49afba'
	channels - set your address channels, separated by ,  ==> 'd3usxm4ch1n4'
	filter - set filter words or event type ==> '0'
	server - set your BLACK server ip:port ==> 'http://block.blackrabbit.is:8888'


 Commands for module 'block':
	genkeys - genkeys
	enc - enc 'message'
	dec - dec 'message'
	send - example (send senderAddress receiverAddress msg)
	cmdsensor - example (cmdsensor eosaddress command_line)
	deploy - example (deploy eosaddress arquitecture sensor_type)
	track - example (track eosaddress task time)
	services - example (services eosaddress)
	receive - example (receive eosaddress)
	core - Example (core get info)
	list_devices - Example (list_devices addr)
	list_payloads - Example (core get info)
	list_event_types - Example (list_event_types)
	list_sensor_types - Example (list_sensor_types)
	upsert_devices - Example (upsert_devices hostname arch event_type services data longitude latitude street city state)
	upsert_payloads - Example (upsert_payloads name description service (code_text|file) )
	upsert_sensor_types - Example (upsert_sensor_types name description)
	upsert_event_types - Example (upsert_event_types name description)
	test_all - 

BlackBlock/block $> 


```


