#!/usr/bin/python3 

import sys
import requests
from bs4 import BeautifulSoup

if len(sys.argv) < 2:
	print("ERROR: You must provide a title to search by")
	exit(1)
elif len(sys.argv) > 2:
	print("ERROR: Too many arguments")
	exit(1)

search_by_title = sys.argv[1]

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
	RFC = {}
	if datas is not []:
		for data, header in zip(datas,headers):
			RFC[header.text] = data.text.replace(u'\xa0', u' ')
		if RFC is not {}:
			RFCS.append(RFC)

for RFC in RFCS:
	print(RFC)
