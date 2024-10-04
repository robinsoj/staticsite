import unittest

from textnode import TextNode

class TestTextNode(unittest.TestCase):
	def test_eq(self):
		node = TextNode("This is a text node", "bold")
		node2 = TextNode("This is a text node", "bold")
		self.assertEqual(node, node2)

	def test_neq(self):
		node = TextNode("This is a text node", "bold")
		node2 = TextNode("This is a text node", "italics")
		self.assertNotEqual(node, node2)

	def test_url_added(self):
		node = TextNode("This is a text node", "bold", "http://google.com")
		node2 = TextNode("This is a text node", "bold", "http://google.com")
		self.assertEqual(node, node2)

	def test_mismatched_url(self):
		node = TextNode("This is a text node", "bold", "http://google.com")
		node2 = TextNode("This is a text node", "bold", "www.bing.com")
		self.assertNotEqual(node, node2)

	def test_repr(self):
		node = TextNode("This is a text node", "bold")
		node2 = TextNode("This is a text node", "bold")
		self.assertEqual(repr(node), repr(node2))

if __name__ == "__main__":
	unittest.main()
