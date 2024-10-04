from htmlnode import HTMLNode

class ParentNode(HTMLNode):
	def __init__(self, tag = None, children = None, props = None):
		super().__init__(tag, None, children, props)

	def to_html(self):
		if (self.tag is None):
			raise ValueError('Tag is required in ParentNodes')
		if (self.children is None):
			raise ValueError('Children are required in ParentNodes')
		if self.props is None:
			ret_text = "<" + self.tag + ">"
		else:
			ret_text = "<" + self.tag + self.props_to_html() + ">"
		for child in self.children:
			ret_text += child.to_html()
		ret_text += "</" + self.tag + ">"
		return ret_text

