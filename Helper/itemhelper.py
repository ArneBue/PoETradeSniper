import sys
import re
import ast
import logging

logger = logging.getLogger(__name__)

def normalizeItem(item, stashName, accountName, lastCharacterName, poeNinjaApi):
	priceDic = normalizeItemPrice(item.get('note', ""), stashName, poeNinjaApi)

	newItem = {'name': normalizeItemName(item.get('name'), item.get('typeLine')),
			   'accountName': accountName,
			   'lastCharacterName': lastCharacterName,
			   'itemType': item.get('frameType'),
			   'note': item.get('note', ''),
           	   'price': priceDic.get('price', 'unpriced'),
			   'origPrice': priceDic.get('origPrice', 'unpriced'),
			   'unit': priceDic.get('unit', 'unpriced'),
			   'xLoc': item.get('x'),
			   'yLoc': item.get('y'),
			   'Links': maxLinks(item.get('sockets')),
			   'stashName': stashName,
               'identified': item.get('identified'),
               'corrupted': item.get('corrupted'),
			   'id': item.get('id'),
			   'mods': normalizeItemMods(item.get('enchantMods'), 
			   							 item.get('implicitMods'), 
										 item.get('explicitMods'), 
										 item.get('craftedMods'), 
										 item.get('corrupted')
										 )
			}
	if 'Yoshi' in lastCharacterName:
		logger.info(newItem)
		logger.info('dic:' + str(priceDic))
	return newItem


def normalizeItemName(name, typeLine):
	if name == "":
		return re.sub(r'<<.*>>', '', typeLine)
	else: 
		return re.sub(r'<<.*>>', '', name)

def normalizeItemPrice(note, stashName, poeNinjaApi):
	if note:
		price = note
	else:
		price = stashName

	if not ('~b/o' in price or '~price' in price):
		return {'price': 'unpriced'}

	price = price.replace("~b/o", "")
	price = price.replace("~price", "")

	price = price.strip()
	
	if not price or '/' in price:
		return {'price': 'unpriced'}
	
	try:
		price, unit = price.split(" ", 1)
		priceFinal = price

		if unit != "chaos":
			convertedPrice = convertToChaos(price, unit, poeNinjaApi)
		else:
			convertedPrice = price

		if isinstance(convertedPrice, basestring) and '.' in convertedPrice:
			convertedPrice = float(convertedPrice)
		else:
			convertedPrice = int(convertedPrice)
	except Exception as e:
		logger.error(e)
		traceback.print_exc()
		return {'price': 'unpriced'}

	return {'price': convertedPrice, 'unit' : unit, 'origPrice': price}


def convertToChaos(price, unit, poeNinjaApi):
	
	if unit == 'exa':
		return float(price) * float(poeNinjaApi.currencyPrices['Exalted Orb'])
	else:
		return 'not priced in chaos'


def normalizeItemMods(enchantMods, implicitMods, explicitMods, craftedMods, corrupted):
	mods = []

	if enchantMods is not None:
		mods.extend(enchantMods)

	if implicitMods is not None:
		mods.extend(implicitMods)

	if explicitMods is not None:
		mods.extend(explicitMods)

	if craftedMods is not None:
		mods.extend(craftedMods)

	if corrupted is not None and corrupted == True:
		mods.extend({"Corrupted"})

	return mods

def maxLinks(sockets):
	groups = {}
	max = 0
	for socket in sockets:
		if socket.get("group") not in groups:
			groups[socket.get("group")] = 1
		else:
			groups[socket.get("group")]+= 1
		
		if groups[socket.get("group")] > max:
			max = groups[socket.get("group")]

	if max != 6 and max != 5:
		max = 0
	return str(max)
		
