from textnode import TextNode
from collections import Counter
from extract_images import *
from split_nodes_delimiter import *
import re

def text_to_textnode(text):
	ret_list = []
	nodes = split_nodes_delimiter([TextNode(text, 'text')], '**', 'bold')
	nodes = split_nodes_delimiter(nodes, '*', 'italic')
	nodes = split_nodes_delimiter(nodes, '`', 'code')
	new_nodes = []
	for node in nodes:
		new_nodes.extend(split_nodes_image([node]))
	nodes = new_nodes;
	new_nodes = []
	for node in nodes:
		new_nodes.extend(split_nodes_link([node]))
	nodes = new_nodes
	return nodes

