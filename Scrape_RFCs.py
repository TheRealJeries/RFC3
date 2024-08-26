#!/usr/bin/python3 

import sys
import requests
from bs4 import BeautifulSoup
import pywebio 
from pywebio.input import input, TEXT
from pywebio.output import put_text, put_html, put_markdown, put_table
import Tree_HTML
import re

more_info_keys=["Obsoleted by", "Obsoletes", "Updated by", "Updates"]

def generate_HTML(RFCS):
	HTML = Tree_HTML.header_html()
	HTML = HTML + Tree_HTML.start_tree()
	for RFC in RFCS:
		if RFC is not {}:
			html_to_paste = RFC["Number"]
			HTML = HTML + Tree_HTML.generate_tree_node(html_to_paste)
	HTML = HTML + Tree_HTML.end_tree()
	HTML = HTML + "</nav>"
	put_html(HTML)

def regex_to_match_RFCs_by(key_word):
	return ".*"+key_word+"\s+(RFC \d+\s*(,\s*RFC \d+)*).*"

def add_more_info_to_RFC(RFCs, RFC, data):
	for key in more_info_keys:
		key_match = re.match(regex_to_match_RFCs_by(key), data)
		if key_match:
			if key not in RFC:
				RFC[key] = []
			action_RFC_nums = key_match.group(1).split(",")
			for action_RFC_num in action_RFC_nums:
				print(RFC["Number"]+"["+key+"] += "+action_RFC_num.strip())
				RFC[key].append(action_RFC_num.strip())

def replace_RFC_nums_with_dicts(RFCs):
	for RFC in RFCs:
		for key in more_info_keys:
			if key in RFC:
				action_RFC_nums = RFC[key]
				for idx, action_RFC_num in enumerate(action_RFC_nums):
					RFC_to_add = get_RFC(RFCs, action_RFC_num)
					if RFC_to_add == {}:
						RFC_to_add = {"Number":action_RFC_num}
					RFC[key][idx] = RFC_to_add

def get_RFC(RFCs, RFC_num):
	for RFC in RFCs:
		if RFC_num in RFC["Number"]:
			#return RFCs.pop(idx)
			return RFC
	print("Could not find "+RFC_num)
	return {}

def create_RFC_dictionary_item(RFCs, datas, headers):
	RFC = {}
	for data, header in zip(datas,headers):
		cleaned_data = data.text.replace(u'\xa0', u' ')
		if header.text == 'More Info':
			add_more_info_to_RFC(RFCs, RFC, cleaned_data)
		RFC[header.text] = cleaned_data
	return RFC

def walk_through_RFCs(RFCs):
	for RFC in RFCs:
		print(RFC["Number"])
		for key in more_info_keys:
			if key in RFC:
				print("\t"+key)
				for action_RFC in RFC[key]:
					print("\t\t"+action_RFC["Number"])

def create_RFC_dictionary(argv):
	#if len(argv) < 2:
	#	print("ERROR: You must provide a title to search by")
	#	exit(1)
	#elif len(argv) > 2:
	#	print("ERROR: Too many arguments")
	#	exit(1)

	#search_by_title = argv[1]
	search_by_title = input("Provide a keyword or title to search by", type=TEXT)

	URL = "http://www.rfc-editor.org/search/rfc_search_detail.php?page=All&title={title}&sortkey=Number&sorting=ASC".format(title=search_by_title)
	page = requests.get(URL).text
	soup = BeautifulSoup(page, 'html.parser')
	table = soup.find("table", "gridtable")
	headers = table.find_all("th")
	rows = table.find_all("tr")

	RFCs = []
	
	for row in rows:
		idx = 0
		datas = row.find_all("td")
		if datas is not [] and len(datas) != 0:
			RFCs.append(create_RFC_dictionary_item(RFCs, datas, headers))

	replace_RFC_nums_with_dicts(RFCs)

	walk_through_RFCs(RFCs)

	return RFCs

if __name__ == '__main__':
	RFCS = create_RFC_dictionary(sys.argv)
	generate_HTML(RFCS)
