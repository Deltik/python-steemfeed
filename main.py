import os
import configparser
import requests
from steem import Steem
from pprint import pprint
from html.parser import HTMLParser
import re

class CoinMarketCapPriceHTMLParser(HTMLParser):
    next_data_is_price = False
    raw_price = ''

    def handle_starttag(self, tag, attrs):
        if tag == 'span' and any(attr[1] == 'cmc-details-panel-price__price' for attr in attrs):
            self.next_data_is_price = True

    def handle_data(self, data):
        if self.next_data_is_price:
            self.raw_price = data
            self.next_data_is_price = False

def main():
    config = configparser.ConfigParser()
    config.read('config.ini')
    config.read('config.secret.ini')
    nodes = config['DEFAULT']['nodes'].split(',')
    keys = config['steem-secrets']['wif_keys'].split(',')
    witness_name = config['steem-secrets']['witness_name']
    wallet_password = config['steem-secrets']['wallet_password']

    result = requests.get('https://coinmarketcap.com/currencies/steem/')
    parser = CoinMarketCapPriceHTMLParser()
    parser.feed(result.text)
    price = re.sub(r'[\$,]', '', parser.raw_price)
    try:
        price = float(price)
    except ValueError:
        print("Could not parse price: %s" % price)
        exit(1)

    if price <= 0:
        print("Price %s is too low!" % price)
        exit(1)

    print("Witness name: %s" % witness_name)
    print("Price received: %s" % price)

    steem = Steem(nodes=nodes, keys=keys)
    wallet = steem.wallet

    steem.commit.witness_feed_publish(price, account=witness_name)

    pprint(steem.get_witness_by_account(witness_name))

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    main()
