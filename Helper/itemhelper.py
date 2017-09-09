import sys
import re
import ast

def normalizeItem(item, stashName, accountName, lastCharacterName):
	newItem = {'name': normalizeItemName(item.get('name'), item.get('typeLine')),
			   'accountName': accountName,
			   'lastCharacterName': lastCharacterName,
			   'itemType': item.get('frameType'),
			   'note': item.get('note', ''),
			   'price': normalizeItemPrice(item.get('note', ""), stashName), 
			   'xLoc': item.get('x'),
			   'yLoc': item.get('y'),
			   'Links': maxLinks(item.get('sockets')),
			   'stashName': stashName,
               'identified': item.get('identified'),
               'corrupted': item.get('corrupted'),
			   'mods': normalizeItemMods(item.get('enchantMods'), 
			   							 item.get('implicitMods'), 
										 item.get('explicitMods'), 
										 item.get('craftedMods'), 
										 item.get('corrupted')
										 )
			}
	return newItem


def normalizeItemName(name, typeLine):
	if name == "":
		return re.sub(r'<<.*>>', '', typeLine)
	else: 
		return re.sub(r'<<.*>>', '', name)

def normalizeItemPrice(note, stashName):
	if note:
		price = note
	else:
		price = stashName

	if not ('~b/o' in price or '~price' in price):
		return 'unpriced'

	price = price.replace("~b/o", "")
	price = price.replace("~price", "")

	price = price.strip()

	if not price or '/' in price:
		return 'unpriced'
	
	try:
		price, unit = price.split(" ", 1)
	except:
		return 'unpriced'

	priceFinal = price

	if unit != "chaos":
		return convertToChaos(price, unit)
	
	if '.' in priceFinal:
		priceFinal = float(priceFinal)
	else:
		priceFinal = int(priceFinal)

	return priceFinal


def convertToChaos(price, unit):
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
		
