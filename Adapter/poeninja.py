import requests
import logging
import time
import sys

logger = logging.getLogger(__name__)

class PoENinja:
    prices = {}

    latestupdate = 0

    def __init__(self, config):
        self.config = config
        self.updatePrices()
        logger.info("Item Price List created")

    def updatePrices(self):
        for (itemType, url) in self.config.items("PoeNinjaApi"):
            self.prices[itemType] = self.getPrices(url)

        latestupdate = time.time()

    def getPrices(self, url):
        ninjaUrl = self.config.get("URL", "PoENinjaAPI") + url

        r = requests.get(ninjaUrl, {
            'league': self.config.get("Config", "league"),
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
        ninjaUrl = self.config.get("URL", "PoENinjaAPI") + self.config.get("URL", "GetStats")

        logger.debug(ninjaUrl)

        r = requests.get(ninjaUrl)
        changeID = r.json().get('nextChangeId')

        logger.info("Starting at: " + changeID)
        return changeID
