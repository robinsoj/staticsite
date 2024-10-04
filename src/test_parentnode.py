import unittest
from parentnode import ParentNode
from leafnode import LeafNode

class TestLeafNode(unittest.TestCase):
	def test_with_children(self):
		node = ParentNode(
			"p",
			[
				LeafNode("b", "Bold text"),
				LeafNode(None, "Normal text"),
				LeafNode("i", "italic text"),
				LeafNode(None, "Normal text"),
				],
			)
		self.assertEqual(node.to_html(), "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>")

	def test_with_props(self):
		node = ParentNode("p",
						  [
							  LeafNode("b", "Bold text"),
							  LeafNode(None, "Normal text"),
							  LeafNode("i", "italic text"),
							  LeafNode(None, "Normal text"),
							  ],
						  {"href": "https://www.google.com"}
						  )
		self.assertEqual(node.to_html(), '<p href="https://www.google.com"><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>')

if __name__ == "__main__":
		unittest.main()

