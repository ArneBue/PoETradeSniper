import logging
import requests
import time
import json

from Helper import itemhelper

logger = logging.getLogger(__name__)

class PoEAPI:

    filters = []

    def __init__(self, config, startID):
        self.config = config
        self.changeID = startID

    def request(self):
        startTime = time.time()
        tradeURL = self.config.get("URL", "TradeApi") + self.changeID

        logger.debug(tradeURL)

        if True:
            r = requests.get(tradeURL)
            data = r.json()
        else:
            with open('public-stash-tabs.json') as data_file:
                logger.warning("Running in Offline Mode")
                data = json.load(data_file)

        self.changeID = data.get('next_change_id', self.changeID)
        logger.info("New Change ID: " + self.changeID)

        self.parseItems(data.get('stashes'))

    def parseItems(self, stashes):
        for stash in stashes:
            accountName = stash.get('accountName')
            lastCharacterName =  stash.get('lastCharacterName')
            stashName = stash.get('stash')
            items = stash.get('items')

            for itemIterator in items:
                if itemIterator.get('league') == self.config.get('Config', 'league'):
                    item = itemhelper.normalizeItem(itemIterator, stashName, accountName, lastCharacterName)
                    self.filter(item)                    

                

    def filter(self, item):
        for filter in self.filters:
            if(filter.checkCondition(item)):
                listedPrice = filter.isWorthBuying(item)
                if(listedPrice):
                    filter.sendMessage(item, listedPrice)

    def addFilter(self, filter):
        self.filters.append(filter)
                
