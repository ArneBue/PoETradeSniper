import logging
import requests
import time
import json
import traceback

from config import config
from Helper import itemhelper

logger = logging.getLogger(__name__)

class PoEAPI:

    filters = []
    itemids = []

    def __init__(self, startID):
        self.changeID = startID

    def request(self):
        startTime = time.time()
        tradeURL = config.get("URL", "TradeApi") + self.changeID

        logger.debug(tradeURL)

        data = self.doRequest(tradeURL)

        self.changeID = data.get('next_change_id', self.changeID)

        logger.info("New Change ID: " + self.changeID)

        try:
            self.parseItems(data.get('stashes'))
        except Exception as e:
            logger.error(e)
            traceback.print_exc()
            with open('public-stash-tabs.json', 'w') as outfile:
                json.dump(data, outfile)

    def doRequest(self, tradeURL):
        if config.get('Config', 'loadErrorStashTab') == 'False':
            startDownload = time.time()
            r = requests.get(tradeURL)
            end = time.time() - startDownload
            data = r.json()
            logger.info("Download took: " + str(end))
        else:
            with open('public-stash-tabs.json') as data_file:
                logger.warn('Error mode')
                data = json.load(data_file)

        return data


    def parseItems(self, stashes):
        for stash in stashes:
            accountName = stash.get('accountName')
            lastCharacterName =  stash.get('lastCharacterName')
            stashName = stash.get('stash')
            items = stash.get('items')

            for itemIterator in items:
                if itemIterator.get('league') == config.get('Config', 'league'):
                    item = itemhelper.normalizeItem(itemIterator, stashName, accountName, lastCharacterName)
                    self.filter(item)                    

                

    def filter(self, item):
        if item.get('id') in self.itemids:
            return False

        for filter in self.filters:
            if(filter.checkCondition(item)):
                listedPrice = filter.isWorthBuying(item)
                if(listedPrice):
                    self.itemids.append(item.get('id'))
                    filter.sendMessage(item, listedPrice)

    def addFilter(self, filter):
        self.filters.append(filter)
                
