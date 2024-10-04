from leafnode import LeafNode

class TextNode:
	def __init__(self, text, text_type, url = None):
		self.text = text
		self.text_type = text_type
		self.url = url

	def __eq__(self, rhs_textnode):
		return self.text == rhs_textnode.text and self.text_type == rhs_textnode.text_type and self.url == rhs_textnode.url

	def __repr__(self):
		return "TextNode(" + str(self.text) + ", " + str(self.text_type) + ", " + str(self.url) + ")"

	def text_node_to_html_node(self):
		match self.text_type:
			case 'text':
				ret_node = LeafNode(None, self.text)
			case 'bold':
				ret_node = LeafNode('b', self.text)
			case 'italic':
				ret_node = LeafNode('i', self.text)
			case 'code':
				ret_node = LeafNode('code', self.text)
			case 'link':
				dictionary['href'] = self.url
				ret_node = LeafNode('a', self.text, dictionary)
			case 'image':
				dictionary['src'] = self.url
				dictionary['alt'] = self.text
				ret_node = LeafNode('img', '', dictionary)
			case _:
				raise Exception('Invalid text_type in TextNode')
		return ret_node

