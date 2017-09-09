def createMessage(item, price):
	msg = "[{}c/{}c - {}%] @{} Hi, I would like to buy your {} listed for {} in Harbinger (stash tab \"{}\"; position: left {}, top {}) -- {} Links: {}".format(price, item.get('price'), round(((price - item.get('price')) / price) * 100), item.get('lastCharacterName'), item.get('name'), item.get('price'), item.get('stashName'), item.get('xLoc'), item.get('yLoc'), item.get('note'), item.get('Links'))

	modsList = createModList(item.get('mods'))

	if len(modsList) > 1:
		msg += "\n" + modsList

	return msg



def createModList(mods):
	modsList = "```"

	for mod in mods:
		modsList += mod + "\n"
	modsList += "```"

	return modsList
