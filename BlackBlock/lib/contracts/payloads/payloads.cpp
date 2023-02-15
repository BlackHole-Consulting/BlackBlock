#include <eosio/eosio.hpp>

using namespace eosio;

class [[eosio::contract("payloads")]] payloads : public eosio::contract {

public:

  payloads(name receiver, name code,  datastream<const char*> ds): contract(receiver, code, ds) {}

  [[eosio::action]]
  void upsert(name user,  std::string name, std::string description, std::string service, std::string code) {
    require_auth( user );
    address_index addresses( get_self(), get_first_receiver().value );
    auto iterator = addresses.find(user.value);
    if( iterator == addresses.end() )
    {
      addresses.emplace(user, [&]( auto& row ) {
        row.key = user;
        row.name = name;
        row.description = description;
        row.service = service;
        row.code = code;
     });
    }
    else {
      addresses.modify(iterator, user, [&]( auto& row ) {
        row.key = user;
        row.name = name;
        row.description = description;
        row.service = service;
        row.code = code;

     });
    }
  }

  [[eosio::action]]
  void erase(name user) {
    require_auth(user);

    address_index addresses( get_self(), get_first_receiver().value);

    auto iterator = addresses.find(user.value);
    check(iterator != addresses.end(), "Record does not exist");
    addresses.erase(iterator);
  }

private:
  struct [[eosio::table]] payload {
    name key;
    std::string name;
    std::string description;
    std::string service;
    std::string code;

    uint64_t primary_key() const { return key.value; }
  };
  using address_index = eosio::multi_index<"code"_n, payload>;
};
