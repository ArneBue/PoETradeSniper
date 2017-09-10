import logging
import sys
import time
from config import config

from Adapter.poeninja import PoENinja
from Filter.poeninjafilter import PoENinjaFilter
from Filter.testfilter import TestFilter
from poeapi.threadhandlerapi import ThreadHandlerAPI

logging.basicConfig(stream=sys.stderr, level=logging.INFO)

def main():
	

	logging.info("Starting Sniper")


	PoENinjaAdapter = PoENinja()

	start = PoENinjaAdapter.getChangeID()
	handler = ThreadHandlerAPI(start, [PoENinjaFilter(PoENinjaAdapter), TestFilter()])
	handler.initThreads()
	handler.runThreads()

	for thread in handler.threads:
		thread.join()


if __name__ == "__main__":
	main()
