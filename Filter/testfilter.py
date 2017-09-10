import logging
import sys

from Helper import message
from Adapter import discord 

from config import config

logger = logging.getLogger(__name__)

class TestFilter:
	def checkCondition(self, item):
		if 'Belly' in item.get('name') and 'Yoshi' in item.get('lastCharacterName'):
			return True
		else:
			return False

	def isWorthBuying(self, item):
		if 'Belly' in item.get('name') and 'Yoshi' in item.get('lastCharacterName'):
			return True
		else:
			return False

	def evaluate(self, priceNinja, priceItem):
		perc_decrease = ((priceNinja - priceItem) / priceNinja) * 100

		if perc_decrease >= 40 and priceNinja - priceItem > 2:
			return 1
		
		return False

	def sendMessage(self, item, price):
		msg = message.createMessage(item, price)
		discord.send(msg, config.get('Discord', 'Webhook'))
		

#{'name': 'Dusk Ichor', 'itemType': 2, 'price': 'unpriced', 'xLoc': 3, 'yLoc': 1, 'Links': 0, 'mods': [
#    '16% increased Mine Damage', '+8% to all Elemental Resistances', '+15% to Lightning Resistance']}
