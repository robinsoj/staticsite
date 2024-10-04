class HTMLNode:
	def __init__(self, tag = None, value = None, children = None, props = None):
		self.tag = tag
		self.value = value
		self.children = children
		self.props = props

	def to_html(self):
		raise NotImplementedErrror("NYI")

	def props_to_html(self):
		ret_text = []
		if self.props is not None:
			for prop in self.props:
				ret_text.append(f' {prop}="{self.props[prop]}"')
		return ''.join(ret_text)

	def __repr__(self):
		if self.tag is None:
			if self.value is None:
				ret_text = self.create_children()
			else:
				ret_text = self.value
		else:
			ret_text = "<" + self.tag + " " + self.props_to_html() + ">" + str(self.value)
			ret_text += self.create_children()
			ret_text += " </" + self.tag + ">"
		return ret_text

	def create_children(self):
		ret_text = ''
		if (self.children is not None):
			if (self.tag is None):
				for child in self.children:
					ret_text += ' ' + child
			else:
				for child in self.children:
					ret_text += repr(child)
		return ret_text


