import logging
import sys
import time

import requests

from config import config

logger = logging.getLogger(__name__)

class PoENinja:
	prices = {}

	latestupdate = 0

	def __init__(self):
		self.updatePrices()

	def updatePrices(self):
		logging.info("Loading PoE Ninja data")
		
		for (itemType, url) in config.items("PoeNinjaApi"):
			self.prices[itemType] = self.getPrices(url)

		latestupdate = time.time()
		logger.info("Item Price List created")

	def getPrices(self, url):
		ninjaUrl = config.get("URL", "PoENinjaAPI") + url

		r = requests.get(ninjaUrl, {
			'league': config.get("Config", "league"),
			'date': time.strftime("%Y-%m-%d")
		})

		return self.parseItem(r.json().get("lines"))

	def parseItem(self, itemJSON):
		returnDic = {'0': {}, '5': {}, '6': {} }

		for item in itemJSON:

			returnDic[str(item.get("links", '0'))].update({
				item.get("name"): item.get("chaosValue")
			})

		return returnDic

	def requiresUpdate(self):
		if(self.latestupdate + (60 * 30) < time.time()):
			return True
		else:
			return False

	def getChangeID(self):
		ninjaUrl = config.get("URL", "PoENinjaAPI") + config.get("URL", "GetStats")

		logger.debug(ninjaUrl)

		r = requests.get(ninjaUrl)
		changeID = r.json().get('nextChangeId')

		logger.info("Starting at: " + changeID)
		return changeID
