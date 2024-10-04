import unittest
from extract_images import *

class TestTextToHTML(unittest.TestCase):
	def test_extract(self):
		markdown_match = extract_markdown_images("This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)")
		self.assertEqual(markdown_match[0], ('rick roll', 'https://i.imgur.com/aKaOqIh.gif'))
		self.assertEqual(markdown_match[1], ('obi wan', 'https://i.imgur.com/fJRm4Vk.jpeg'))

	def test_link(self):
		link_match = extract_markdown_links("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)")
		self.assertEqual(link_match[0], ('to boot dev', 'https://www.boot.dev'))
		self.assertEqual(link_match[1], ('to youtube', 'https://www.youtube.com/@bootdotdev'))


if __name__ == "__main__":
		unittest.main()

