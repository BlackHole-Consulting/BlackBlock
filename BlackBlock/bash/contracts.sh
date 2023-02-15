#Install the eosio.token contract

cleos set contract eosio.token ~/eosio.contracts/build/contracts/eosio.token/

#Set the eosio.msig contract

cleos set contract eosio.msig ~/eosio.contracts/build/contracts/eosio.msig/

#Create and allocate the SYS currency , CON

cleos push action eosio.token create '[ "eosio", "5000000000.0000 BALBOA" ]' -p eosio.token@active

cleos push action eosio.token issue '[ "eosio", "5000000000.0000 BALBOA", "memo" ]' -p eosio@active

curl -X POST http://127.0.0.1:8888/v1/producer/schedule_protocol_feature_activations -d '{"protocol_features_to_activate": ["0ec7e080177b2c02b278d5088611686b49d739925a92d9bfcacd7fc6b74053bd"]}' | jq

