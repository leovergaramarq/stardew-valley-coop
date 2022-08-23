from os import path as os_path, sep as os_sep
import xml.etree.ElementTree as ET
import copy

def parse_xmlns(file):
	"""
	Parses the xml file path and keeps the namespace 'xmlns:xsd="http://www.w3.org/2001/XMLSchema"'
	https://stackoverflow.com/questions/56553934/how-to-write-to-xml-file-while-keeping-the-existing-namespaces
	"""
	events = "start", "start-ns"
	root = None
	ns_map = []

	for event, elem in ET.iterparse(file, events):
		if event == "start-ns":
			ns_map.append(elem)
		elif event == "start":
			if root is None:
				root = elem
			for prefix, uri in ns_map:
				# originally without the if statement
				if prefix == 'xsd': elem.set("xmlns:" + prefix, uri)
			ns_map = []

	return ET.ElementTree(root)

def main():
	folder_path = os_path.normpath(input('Folder/file path:\n> ').strip())
	
	# Getting file path in case a directory is received 
	if os_path.isdir(folder_path): #If path is a directory, the game file must be called the same
		file_path = os_path.join(folder_path, folder_path.split(os_sep)[-1])
	elif os_path.isfile(folder_path):
		file_path = folder_path
		folder_path = os_path.dirname(folder_path)
	else:
		print('Game file not found')
		return

	# Parsing the xml file
	tree = parse_xmlns(file_path)
	root = tree.getroot()

	# Getting player info
	player = root.find('player')
	player = {
		'node': player,
		'index': list(root).index(player)
	}

	# Getting farmhands info
	farmhands = []
	for indoor in root.findall('./locations/GameLocation/buildings/Building/indoors'):
		farmhand = indoor.find('farmhand')
		farmhands.append({
			'index': list(indoor).index(farmhand),
			'name': farmhand.find('name').text,
			'parent': indoor,
			'node': farmhand
		})

	farmhands_names = [f['name'] for f in farmhands]
	host = input('Who will be hosting? (' + ', '.join(farmhands_names) + ')\n> ').strip()
	if host not in farmhands_names: #Validating new host name
		print('Invalid name')
		return

	# Whether altering 'SaveGameInfo' file or not
	alter_svi = input('(Optional) Want to make a complete change? (y/n)\n> ').strip().lower() == 'y'

	print('Please, wait...')
	farmhand = [f for f in farmhands if f['name'] == host][0]

	# Switching tags
	root.remove(player['node'])
	root.insert(player['index'], farmhand['node'])
	farmhand['parent'].remove(farmhand['node'])
	farmhand['parent'].insert(farmhand['index'], player['node'])

	# Renaming tags
	player['node'].tag = 'farmhand'
	farmhand['node'].tag = 'player'

	# Final indentation and writing file
	ET.indent(tree, space='\t', level=0)
	tree.write(file_path, encoding='utf-8', xml_declaration=True)

	if alter_svi:
		file_svi_path = os_path.join(folder_path, 'SaveGameInfo')
		if not os_path.isfile(file_svi_path): #Validating 'SaveGameInfo' file existance
			print('Couldn\'t find "SaveGameInfo" file (' + file_path + ')')
			return
		
		# farmer = copy.deepcopy(farmhand['node']) #Just in case
		
		# Parsing the xml file
		tree_svi = parse_xmlns(file_svi_path)
		root_svi = tree_svi.getroot()

		# Replacing all child elements
		for el in root_svi.findall('*'): root_svi.remove(el)
		for el in farmhand['node'].findall('*'): root_svi.append(el)

		# Final indentation and writing file
		ET.indent(tree_svi, space='\t', level=0)
		tree_svi.write(file_svi_path, encoding='utf-8', xml_declaration=True)

	print('Say hello to the new admin, ' + host + '!')

if __name__ == '__main__':
	main()
