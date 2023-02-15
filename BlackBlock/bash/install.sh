 #!/bin/bash
 
apt install python3 python3-dev python3-pip cmake make jq
pip3 install git+https://github.com/eosnewyork/eospy.git
apt install curl cmake vim htop jq
pip3 install -r requirements.txt

## debian links for eos install
ln -s /usr/sbin/ldconfig /usr/bin/ldconfig

ln -s /usr/sbin/start-stop-daemon /usr/bin/start-stop-daemon

rhopath=`pwd`
## Install dependences
apt install curl cmake vim htop jq

cd ~
## install eos base

git clone https://github.com/EOSIO/eosio.contracts.git

cd ./eosio.contracts/
git checkout release/1.9.x

./build.sh
cd ./build/contracts/
pwd

cd ~

wget https://github.com/eosio/eosio.cdt/releases/download/v1.8.1/eosio.cdt_1.8.1-1-ubuntu-18.04_amd64.deb

wget https://github.com/eosio/eos/releases/download/v2.2.0-rc1/eosio_2.2.0-rc1-ubuntu-20.04_amd64.deb

dpkg -i eosio*.deb

cd $rhopath

cd bash