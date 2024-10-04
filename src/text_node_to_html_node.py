from leafnode import LeafNode
from htmlnode import HTMLNode
from textnode import TextNode

def text_node_to_html_node(text_node):
	match text_node.text_type:
		case 'text':
			ret_node = LeafNode(None, text_node.text)
		case 'bold':
			ret_node = LeafNode('b', text_node.text)
		case 'italic':
			ret_node = LeafNode('i', text_node.text)
		case 'code':
			ret_node = LeafNode('code', text_node.text)
		case 'link':
			dictionary = dict()
			dictionary['href'] = text_node.url
			ret_node = LeafNode('a', text_node.text, dictionary)
		case 'image':
			dictionary = dict()
			dictionary['src'] = text_node.url
			dictionary['alt'] = text_node.text
			ret_node = LeafNode('img', '', dictionary)
		case _:
			raise Exception('Invalid text_type in TextNode')
	return ret_node

