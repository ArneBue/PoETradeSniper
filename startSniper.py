import logging
import sys
import time
from config import config

from Adapter.poeninja import PoENinja
from Adapter.poeapi import PoEAPI
from Filter.poeninjafilter import PoENinjaFilter
from Filter.testfilter import TestFilter


def main():
	logging.basicConfig(stream=sys.stderr, level=logging.INFO)

	logging.info("Starting Sniper")


	PoENinjaAdapter = PoENinja()

	start = PoENinjaAdapter.getChangeID()

	trade = PoEAPI(start)

	trade.addFilter(PoENinjaFilter(PoENinjaAdapter))
	trade.addFilter(TestFilter())
	while True:
		start_time = time.time()
		trade.request()
		end_time = time.time() - start_time

		logging.info("Everything took: " + str(end_time))
		#if PoENinjaAdapter.requiresUpdate():
			#PoENinjaAdapter.updatePrices()
		if((end_time ) < 1.0):
			time.sleep(1.0 - (end_time))

if __name__ == "__main__":
	main()
