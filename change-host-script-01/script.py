from io import open as io_open
from os import path as os_path, sep as os_sep
from re import search as re_search, finditer as re_finditer
from xml.dom.minidom import parseString

# Main tags
TAG_PLAYER = ['<player>', '</player>']
TAG_FARMHAND = ['<farmhand>', '</farmhand>']

def find_tag_info(xml, tag):
	"""Returns the starting and ending index (and the text of the 'name' tag) of tags received in the xml string"""

	def get_info(it):
		start = it.start()
		end = xml.find(tag[1], start) + len(tag[1])
		m = re_search('<name>(.+?)</name>', xml[start:end])
		name = m.group(1)

		return {'start': start, 'end': end, 'name': name}
	
	return [get_info(m) for m in re_finditer(tag[0], xml)]

def parse_xml(str):
	"""Returns an xml string parsed"""
	return '\n'.join([line for line in parseString(str).toprettyxml().split('\n') if line.strip()])

def main():
	file_path = input('Folder/file path:\n> ').strip()
	
	# Getting file path in case a directory is received 
	if os_path.isdir(file_path):
		file_path = os_path.join(file_path, os_path.normpath(file_path).split(os_sep)[-1])

	try:
		file_r = io_open(file_path, 'r', encoding='utf-8')
	except FileNotFoundError as e:
		print("File not found")
		print(e)
		return
	
	xml = file_r.read()
	file_r.close()

	# Getting host and farmhands information
	host_info = find_tag_info(xml, TAG_PLAYER)[0]
	farmhands_info = find_tag_info(xml, TAG_FARMHAND)

	# Getting all farmhands names and asking which one should be the new host
	farmhands_names = [x['name'] for x in farmhands_info]
	new_host = input('New host (' + ', '.join(farmhands_names) + '):\n> ').strip()
	if(new_host not in farmhands_names):
		print('Non valid player name. Please, check options again.')
		return
	new_host_info = [x for x in farmhands_info if x['name'] == new_host][0]

	print('Please wait...')

	host_info['xml'] = xml[host_info['start']:host_info['end']].replace(TAG_PLAYER[0], TAG_FARMHAND[0]).replace(TAG_PLAYER[1], TAG_FARMHAND[1])
	new_host_info['xml'] = xml[new_host_info['start']:new_host_info['end']].replace(TAG_FARMHAND[0], TAG_PLAYER[0]).replace(TAG_FARMHAND[1], TAG_PLAYER[1])

	# String slicing xd
	xml = xml[:host_info['start']] + new_host_info['xml'] + xml[host_info['end']:new_host_info['start']] + host_info['xml'] + xml[new_host_info['end']:]
	xml = parse_xml(xml)

	file_w = io_open(file_path, 'w', encoding='utf-8')
	file_w.write(xml)
	file_w.close()

	print('Say hello to the new admin, ' + new_host + '!')

if __name__ == '__main__':
	main()
