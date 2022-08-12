import sys
import io
from xml.dom.minidom import parseString
import re

PLAYER = ['<player>', '</player>']
FARMHAND = ['<farmhand>', '</farmhand>']

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
	# file_name = input('File name:\n> ')
	file_name = 'xml_test'

	try:
		file_r = io.open(file_name, mode='r', encoding='utf-8')
	except FileNotFoundError as e:
		print(e)
		return
	
	file_content = file_r.read()
	file_w = io.open(file_name, mode='w', encoding='utf-8')

	if input('Format xml? (y/n)\n> ').lower() == 'y':
		print('Formatting...')
		try:
			file_content = parse_xml(file_content)
		except xml.parsers.expat.ExpatError as e:
			print(e)
			return
		# file_w.write(file_content)
		print('Xml succesfully formatted')
	else: print('Xml will not be formatted')

	# host = input('New host:\n> ')
	print(find_tag_info(file_content, PLAYER))
	print(find_tag_info(file_content, FARMHAND))

	file_w.write(file_content)

	file_r.close()
	file_w.close()

if __name__ == '__main__':
	main()
