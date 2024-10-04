import unittest
from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
	def test_eq(self):
			node = HTMLNode("h1", "test line")
			node2 = HTMLNode("h1", "test line")
			self.assertEqual(repr(node), repr(node2))

	def test_neq(self):
			node = HTMLNode("h1", "test line")
			node2 = HTMLNode("h1", "test line2")
			self.assertNotEqual(repr(node), repr(node2))

	def test_chilren_added(self):
			child = HTMLNode('td', 'A')
			node = HTMLNode("tr", None, [child, child, child])
			node2 = HTMLNode("tr", None, [child, child, child])
			self.assertEqual(repr(node), repr(node2))

	def test_mismatched_children(self):
		child = HTMLNode('td', 'A')
		node = HTMLNode("tr", None, [child, child, child])
		node2 = HTMLNode("tr", None, [child, child])
		self.assertNotEqual(repr(node), repr(node2))

	def test_props(self):
		props = {}
		props['x'] = 'X-Files'
		props['y'] = 'Old Yeller'
		node = HTMLNode("h1", "Movies", None, props)
		node2 = HTMLNode("h1", "Movies", None, props)
		self.assertEqual(repr(node), repr(node2))

if __name__ == "__main__":
		unittest.main()

