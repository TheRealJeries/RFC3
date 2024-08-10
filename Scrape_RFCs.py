#!/usr/bin/python3 

import sys
import requests
from bs4 import BeautifulSoup
import pywebio 
from pywebio.input import input, TEXT
from pywebio.output import put_text, put_html, put_markdown, put_table
import Tree_HTML

def generate_HTML(RFCS):
	HTML = Tree_HTML.header_html() 
	HTML = HTML + Tree_HTML.start_tree()
	for RFC in RFCS:
		if RFC is not {}:
			HTML = HTML + Tree_HTML.generate_tree_node(RFC["Number"])
	HTML = HTML + Tree_HTML.end_tree()
	HTML = HTML + "</nav>"
	put_html(HTML)

def create_RFC_dictionary_item(datas, headers):
	RFC = {}
	for data, header in zip(datas,headers):
		RFC[header.text] = data.text.replace(u'\xa0', u' ')
	return RFC

def create_RFC_dictionary(argv):
	#if len(argv) < 2:
	#	print("ERROR: You must provide a title to search by")
	#	exit(1)
	#elif len(argv) > 2:
	#	print("ERROR: Too many arguments")
	#	exit(1)

	#search_by_title = argv[1]
	search_by_title = input("Provide a keyword or title to search by", type=TEXT)

	URL = "http://www.rfc-editor.org/search/rfc_search_detail.php?title={title}".format(title=search_by_title)
	page = requests.get(URL).text
	soup = BeautifulSoup(page, 'html.parser')
	table = soup.find("table", "gridtable")
	headers = table.find_all("th")
	rows = table.find_all("tr")

	RFCS = []
	
	for row in rows:
		idx = 0
		datas = row.find_all("td")
		if datas is not [] and len(datas) != 0:
			RFCS.append(create_RFC_dictionary_item(datas, headers))
	return RFCS

if __name__ == '__main__':
	RFCS = create_RFC_dictionary(sys.argv)
	print(RFCS)
	generate_HTML(RFCS)
