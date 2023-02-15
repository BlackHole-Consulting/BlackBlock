from aioeos import EosAccount

account = EosAccount(private_key='your key')



routes = []

network_pubkeys = [""]

rules = ["delay","reject","allow","verify"]

reject_point = 66
reject_rules = ["reject"]

warning_point = 33
warning_rules = ["delay","verify"]

allow_point = 32
allow_rules = ["allow"]



