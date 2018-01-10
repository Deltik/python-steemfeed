import os
import configparser
import requests
from steem import Steem
from pprint import pprint

def main():
    config = configparser.ConfigParser()
    config.read('config.ini')
    config.read('config.secret.ini')
    nodes = config['DEFAULT']['nodes'].split(',')
    keys = config['steem-secrets']['wif_keys'].split(',')
    witness_name = config['steem-secrets']['witness_name']
    wallet_password = config['steem-secrets']['wallet_password']

    result = requests.get('https://api.coinmarketcap.com/v1/ticker/steem/')
    price = result.json()[0]['price_usd']
    try:
        price = float(price)
    except ValueError:
        print("Could not parse price: %s" % price)
        exit(1)

    if price <= 0:
        print("Price %s is too low!" % price)
        exit(1)

    print("Price received: %s" % price)

    steem = Steem(nodes=nodes, keys=keys)
    wallet = steem.wallet

    # Workaround for library bug
    from steembase.storage import MasterPassword
    wallet.MasterPassword = MasterPassword

    wallet.masterpassword = MasterPassword(wallet_password).decrypted_master
    # End workaround

    steem.commit.witness_feed_publish(price, account=witness_name)

    pprint(steem.get_witness_by_account(witness_name))

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    main()
