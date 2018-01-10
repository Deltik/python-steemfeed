Python STEEM Price Feed Updater
===

[![GitHub releases](https://img.shields.io/github/release/Deltik/steemfeed-python.svg)](https://github.com/Deltik/steemfeed-python/releases)

**Python STEEM Price Feed Updater** (`python-steemfeed`) is a simple oneshot script that obtains the current USD [price of STEEM from CoinMarketCap](https://coinmarketcap.com/currencies/steem/) and uses the price value to update a Steem witness's price feed.

This script is best used with a job scheduler like [cron](https://en.wikipedia.org/wiki/Cron) so that the witness's price feed stays up-to-date.

## Installation

1. Choose the destination where you want the script installed:

       $ cd ~
       $ pwd
       /home/steem
       
2. Clone this repository:

       git clone https://github.com/Deltik/python-steemfeed.git

3. Edit `python-steemfeed/config.secret.ini` with the following required information:

       [steem-secrets]
       wif_keys = <the active private key of your witness>
       witness_name = <the name of your witness>
       wallet_password = <the password to the wallet of the witness>
       
4. (_Optional_) Edit `python-steemfeed/config.ini` with a comma-delimited (`,`) list of RPC servers you want to use.  Default:

       [DEFAULT]
       nodes = https://api.steemit.com,https://steemd.steemitstage.com,https://steemd.steemitdev.com
       
5. Set up a cron job to run the script `python-steemfeed/main.py` every five minutes (`*/5 * * * *`):

       $ crontab -e
       
   Input:
       
       */5 * * * * cd /home/steem/python-steemfeed && ./bin/python main.py
   
   **Note:** Change `/home/steem` to the path where you put the `python-steemfeed` repository.

## Compatibility

### Compatible Operating Systems

This repository was designed for the following 64-bit operating systems:
* Debian 7 Wheezy through Debian 11 Bullseye
* Ubuntu 14.04 Trusty Tahr through Ubuntu 18.04 Bionic Beaver

If you have a compatible operating system, all Python dependencies are already packaged in this repository.  You can enter the [virtualenv](https://virtualenv.pypa.io/) to do development like so:

    cd ./python-steemfeed
    source ./bin/activate

The operating systems listed above should be able to install any necessary shared libraries through `apt` if they are not already installed.  These should be the library packages needed:

* libbz2-1.0
* libc6
* libexpat1
* liblzma5
* libncursesw5
* libssl1.0.0
* libtinfo5
* zlib1g

They can be installed with:

    sudo apt install -y libbz2-1.0 libc6 libexpat1 liblzma5 libncursesw5 libssl1.0.0 libtinfo5 zlib1g

### Other Operating Systems

If you have a different operating system or dependent shared libraries are not properly installed in the compatible operating systems above, you will need to install Python 3.6 with SSL support and [pip](https://en.wikipedia.org/wiki/Pip_(package_manager)) for Python 3, then install the dependencies with:

    cd ./python-steemfeed
    pip install -r requirements.txt

Then use the Python 3.6 you installed to execute the price feed updater:

    python main.py
