#!/bin/bash
if [ $# -eq 0 ]; then
    echo "Usage : ./compile.sh account public_key"
    exit 1
fi

# get variables
acc=$1
pubkey=$2

## payloads contract
cd payloads
eosio-cpp payloads.cpp -abigen -abigen_output=payloads.abi  -o=payloads.wasm
cleos create account $acc payloads $pubkey -p $acc@active

## devices contract
cd ..
cd devices
eosio-cpp devices.cpp -abigen -abigen_output=devices.abi  -o=devices.wasm
cleos create account $acc devices $pubkey -p $acc@active

## sensors concrat
cd ..
cd sensors
eosio-cpp sensors.cpp -abigen -abigen_output=sensors.abi  -o=sensors.wasm
cleos create account $acc sensors $pubkey -p $acc@active


## events contract
cd ..
cd events
eosio-cpp events.cpp -abigen -abigen_output=events.abi  -o=events.wasm
cleos create account $acc events $pubkey -p $acc@active



##
cd ..


cleos set contract payloads payloads -p payloads@active
cleos set contract devices devices -p devices@active
cleos set contract events events -p events@active
cleos set contract sensors sensors -p sensors@active
