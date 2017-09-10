import logging
import sys

from Helper import message
from Adapter import discord 

from config import config

logger = logging.getLogger(__name__)

class TestFilter:
	def checkCondition(self, item):
		if item.get('price') == 0:
			return False

		if 'Piece of' in item.get('name') or 'Ventor\'s' in item.get('name'):
			return False

		if 'Tabula' in item.get('name') and item.get('price') != 'unpriced' and item.get('price') != 'not priced in chaos':
			return True

		if item.get('corrupted') is not None and item.get('corrupted') == True:
			return False

		if item.get('itemType') == 3 or item.get('itemType') == 6:
			if item.get('price') != 'unpriced' and item.get('price') != 'not priced in chaos' and item.get('identified'):
				return True

		return False

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
