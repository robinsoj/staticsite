import unittest
from parentnode import ParentNode
from leafnode import LeafNode
from textnode import TextNode

class TestTextToHTML(unittest.TestCase):
	def test_text(self):
		node = TextNode('Text only', 'text', None)
		result = node.text_node_to_html_node()
		self.assertIsInstance(result, LeafNode)
		self.assertEqual(result.tag, None)
		self.assertEqual(result.to_html(), 'Text only')

if __name__ == "__main__":
		unittest.main()

