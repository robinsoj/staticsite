from htmlnode import HTMLNode

class LeafNode(HTMLNode):
	def __init__(self, tag = None, value = None, props = None):
		super().__init__(tag, value, None, props)

	def to_html(self):
		if (self.value is None):
			raise ValueError('Value is required in LeafNodes')
		ret_text = ''
		if (self.tag is None):
			ret_text = self.value
		else:
			if self.props is None:
				ret_text = ("<" + self.tag + ">" + str(self.value) + "</" + self.tag + ">")
			else:
				ret_text = ("<" + self.tag + self.props_to_html() + ">" + str(self.value) + "</" + self.tag + ">")
		return ret_text

