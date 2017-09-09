import logging
import sys
import time
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
		start_time = time.time()
		trade.request()
		end_time = time.time() - start_time

		logging.info("Download took: " + str(end_time))
		#if PoENinjaAdapter.requiresUpdate():
			#PoENinjaAdapter.updatePrices()
		if((end_time ) < 1.0):
			time.sleep(1.0 - (end_time))

if __name__ == "__main__":
	main()
