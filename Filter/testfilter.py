import logging
import sys

from Helper import message
from Adapter import discord 

from config import config

logger = logging.getLogger(__name__)

class TestFilter:
	def checkCondition(self, item):
		return (item.get('name') == 'Belly of the Beast' and item.get('price') is not 'unpriced' and item.get('price') is not 'not priced in chaos')

	def isWorthBuying(self, item):
		if item.get('name') == 'Belly of the Beast' and int(item.get('price')) > 5000:
			return True
		else:
			return False

	def sendMessage(self, item, price):
		msg = "Found: " + item.get('name') + " from " + item.get('lastCharacterName')
		discord.send(msg, config.get('Discord', 'Webhook'))
		

#{'name': 'Dusk Ichor', 'itemType': 2, 'price': 'unpriced', 'xLoc': 3, 'yLoc': 1, 'Links': 0, 'mods': [
#    '16% increased Mine Damage', '+8% to all Elemental Resistances', '+15% to Lightning Resistance']}
