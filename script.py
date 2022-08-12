import sys
import io
from xml.dom.minidom import parseString
import re

TAG_PLAYER = ['<player>', '</player>']
TAG_FARMHAND = ['<farmhand>', '</farmhand>']

def find_tag_info(xml, tag):
	def get_info(it):
		start = it.start()
		end = xml.find(tag[1], start) + len(tag[1])
		m = re.search('<name>(.+?)</name>', xml[start:end])
		name = m.group(1)

		return {'start': start, 'end': end, 'name': name}
	
	return [get_info(m) for m in re.finditer(tag[0], xml)]

def parse_xml(str):
	return '\n'.join([line for line in parseString(str).toprettyxml().split('\n') if line.strip()])

def main():
	file_name = input('File name:\n> ')
	# file_name = 'xml_test'

	try:
		file_r = io.open(file_name, mode='r', encoding='utf-8')
	except FileNotFoundError as e:
		print(e)
		return
	
	xml = file_r.read()

	if input('Format xml? (y/n)\n> ').lower() == 'y':
		print('Formatting...')
		try:
			xml = parse_xml(xml)
		except xml.parsers.expat.ExpatError as e:
			print(e)
			return
		# file_w.write(xml)
		print('Xml succesfully formatted')
	else: print('Xml will not be formatted')

	host_info = find_tag_info(xml, TAG_PLAYER)[0]
	farmhands_info = find_tag_info(xml, TAG_FARMHAND)

	farmhands_names = list(map(lambda x: x['name'], farmhands_info))
	new_host = input('New host ('+', '.join(farmhands_names)+'):\n> ').strip()
	
	if(new_host not in farmhands_names):
		print('Non valid player name. Please, check options again.')
		return

	new_host_info = [i for i in farmhands_info if i['name'] == new_host][0]

	print(new_host_info)

	host_info['xml'] = xml[host_info['start']:host_info['end']].replace(TAG_PLAYER[0], TAG_FARMHAND[0]).replace(TAG_PLAYER[1], TAG_FARMHAND[1])
	new_host_info['xml'] = xml[new_host_info['start']:new_host_info['end']].replace(TAG_FARMHAND[0], TAG_PLAYER[0]).replace(TAG_FARMHAND[1], TAG_PLAYER[1])

	xml = xml[:host_info['start']] + new_host_info['xml'] + xml[host_info['end']:new_host_info['start']] + host_info['xml'] + xml[new_host_info['end']:]
	xml = parse_xml(xml)

	file_w = io.open(file_name, mode='w', encoding='utf-8')
	file_w.write(xml)

	file_r.close()
	file_w.close()

	print(new_host_info['name'] + ' is now the host!')

if __name__ == '__main__':
	main()
