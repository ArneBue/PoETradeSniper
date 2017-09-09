import logging
import sys

from configparser import ConfigParser

from Adapter.poeninja import PoENinja
from Adapter.poeapi import PoEAPI
from Filter.poeninjafilter import PoENinjaFilter


def main():
    logging.basicConfig(stream=sys.stderr, level=logging.INFO)

    logging.info("Starting Sniper")
    logging.info("Parsing Configuration File")
    config = ConfigParser()
    config.read('config.ini')

    PoENinjaAdapter = PoENinja(config)

    start = PoENinjaAdapter.getChangeID()

    trade = PoEAPI(config, start)

    trade.addFilter(PoENinjaFilter(PoENinjaAdapter))
    while True:
        trade.request()

        #if PoENinjaAdapter.requiresUpdate():
            #PoENinjaAdapter.updatePrices()

if __name__ == "__main__":
    main()
