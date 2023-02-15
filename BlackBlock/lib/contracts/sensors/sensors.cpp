#include <eosio/eosio.hpp>

using namespace eosio;

class [[eosio::contract("sensor_types")]] sensor_types : public eosio::contract {

public:

  sensor_types(name receiver, name code,  datastream<const char*> ds): contract(receiver, code, ds) {}

  [[eosio::action]]
  void upsert(name user,  std::string name, std::string description) {
    require_auth( user );
    address_index addresses( get_self(), get_first_receiver().value );
    auto iterator = addresses.find(user.value);
    if( iterator == addresses.end() )
    {
      addresses.emplace(user, [&]( auto& row ) {
        row.key = user;
        row.name = name;
        row.description = description;
     });
    }
    else {
      addresses.modify(iterator, user, [&]( auto& row ) {
        row.key = user;
        row.name = name;
        row.description = description;

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
  struct [[eosio::table]] stype {
    name key;
    std::string name;
    std::string description;

    uint64_t primary_key() const { return key.value; }
  };
  using address_index = eosio::multi_index<"sensors"_n, stype>;
};
