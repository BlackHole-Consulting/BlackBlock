#include <eosio/eosio.hpp>

using namespace eosio;

class [[eosio::contract("devices")]] devices : public eosio::contract {

public:

  devices(name receiver, name code,  datastream<const char*> ds): contract(receiver, code, ds) {}

  [[eosio::action]]
  void upsert(name user,  std::string hostname,std::string arch, std::string event_type, std::string services,std::string data,std::string lt,std::string lat, std::string street, std::string city, std::string state) {
    require_auth( user );
    address_index addresses( get_self(), get_first_receiver().value );
    auto iterator = addresses.find(user.value);
    if( iterator == addresses.end() )
    {
      addresses.emplace(user, [&]( auto& row ) {
       row.key = user;
       row.hostname = hostname;
       row.arch = arch;
       row.event_type = event_type;
       row.services = services;
       row.data = data;
       row.lt = lt;
       row.lat = lat;
       row.street = street;
       row.city = city;
       row.state = state;
     });
    }
    else {
      addresses.modify(iterator, user, [&]( auto& row ) {
       row.key = user;
       row.hostname = hostname;
       row.arch = arch;
       row.event_type = event_type;
       row.services = services;
       row.data = data;
       row.lt = lt;
       row.lat = lat;
       row.street = street;
       row.city = city;
       row.state = state;

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
  struct [[eosio::table]] sensor {
    name key;
    std::string hostname;
    std::string arch;
    std::string event_type;
    std::string services;
    std::string data;
    std::string lt;
    std::string lat;
    std::string street;
    std::string city;
    std::string state;

    uint64_t primary_key() const { return key.value; }
  };
  using address_index = eosio::multi_index<"sensors"_n, sensor>;
};
