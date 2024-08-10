#!/usr/bin/python3

import os

HEADER_HTML = "<link href='https://fonts.googleapis.com/css?family=Fjalla+One' rel='stylesheet' type='text/css'>\n"
HEADER_HTML = HEADER_HTML + "<meta name='viewport' content='width=device-width, initial-scale=1'>\n"
HEADER_HTML = HEADER_HTML + "<link rel='stylesheet' href='https://cdnjs.cloudflare.com/ajax/libs/normalize/5.0.0/normalize.min.css'>\n"
HEADER_HTML = HEADER_HTML + "<link rel='stylesheet' href='https://codepen.io/joellesenne/pen/pdMPdW.css'>"
HEADER_HTML = HEADER_HTML + "<style>"
with open('css/tree_style.css') as f: HEADER_HTML = HEADER_HTML + f.read()
HEADER_HTML = HEADER_HTML + "</style>"
HEADER_HTML = HEADER_HTML + "<nav class='nav'>"


def indent(num_times):
	tabs = ""
	i = 0
	while i < num_times:
		tabs = tabs + "\t"
		i = i + 1
	return tabs

def start_tree():
	return "<ul>"

def end_tree():
	return "</ul>"

def generate_tree_node(text):
	return "<li>" + text + "</li>"

def header_html():
	return HEADER_HTML
