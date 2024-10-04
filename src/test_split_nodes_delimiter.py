import unittest
from textnode import TextNode
from split_nodes_delimiter import *
from text_to_textnode import *

class TestSplitNode(unittest.TestCase):
	def test_single_delimiter(self):
		node = TextNode("This is text with a `code block` word", "text")
		new_nodes = split_nodes_delimiter([node], "`", "code")
		self.assertEqual(len(new_nodes), 3)

	def test_multi_delimiter(self):
		node = TextNode("This is text with a **bolded phrase** in the middle", "text")
		new_nodes = split_nodes_delimiter([node], "**", "bold")
		self.assertEqual(len(new_nodes), 3)

	def test_one_line(self):
		node = TextNode("There are no delimiters", "text")
		new_nodes = split_nodes_delimiter([node], '*', 'italic')
		self.assertEqual(len(new_nodes), 1)

	def test_odd_delimiters(self):
		node = TextNode("Oops! One delimiter", "text")
		with self.assertRaises(Exception):
			new_nodes = split_nodes_delimiter([node], '!', 'h1')

	def test_split_image(self):
		node = TextNode("This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)", 'text')
		new_nodes = split_nodes_image([node])
		self.assertEqual(len(new_nodes), 4)
		self.assertEqual(new_nodes[1], TextNode('rick roll', 'image', 'https://i.imgur.com/aKaOqIh.gif'))
		self.assertEqual(new_nodes[3], TextNode('obi wan', 'image', 'https://i.imgur.com/fJRm4Vk.jpeg'))

	def test_split_link(self):
		node = TextNode("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)", 'text')
		new_nodes = split_nodes_link([node])
		self.assertEqual(len(new_nodes), 4)
		self.assertEqual(new_nodes[1], TextNode('to boot dev', 'link', 'https://www.boot.dev'))
		self.assertEqual(new_nodes[3], TextNode('to youtube', 'link', 'https://www.youtube.com/@bootdotdev'))

	def test_text_to_textnode(self):
		txt = 'This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)'
		type_list = ['text', 'bold', 'text', 'italic', 'text', 'code', 'text',
					 'image', 'text', 'link']
		new_nodes = text_to_textnode(txt)
		self.assertEqual(len(new_nodes), 10)
		for i, node in zip(range(0, 10), new_nodes):
			self.assertEqual(node.text_type, type_list[i])

	def test_markdown_to_blocks(self):
		text = """# This is a heading







	This is a paragraph of text. It has some **bold** and *italic* words inside of it.   

* This is the first list item in a list block
* This is a list item
* This is another list item"""
		mdl = markdown_to_blocks(text)
		self.assertEqual(len(mdl), 3)
		self.assertEqual(mdl[0], '# This is a heading')
		self.assertEqual(len(mdl[2].split('\n')), 3)
		self.assertEqual(mdl[1], 'This is a paragraph of text. It has some **bold** and *italic* words inside of it.')

	def test_btbt(self):
		self.assertEqual(block_to_block_type('``` ```'), 'code')
		self.assertEqual(block_to_block_type('```\n\n\n```'), 'code')
		self.assertEqual(block_to_block_type('`elflang`'), 'paragraph')
		self.assertEqual(block_to_block_type('``` '), 'paragraph')
		self.assertEqual(block_to_block_type('1. Hello\n2.World'), 'ordered list')
		self.assertEqual(block_to_block_type('1. Hello\n3.World'), 'paragraph')
		self.assertEqual(block_to_block_type('* \n- \n* 1'), 'unordered list')
		self.assertEqual(block_to_block_type('* \n* \n* \n* \n* \n* Test'), 'unordered list')
		self.assertEqual(block_to_block_type('# Heading 1'), 'heading')
		self.assertEqual(block_to_block_type('###### Heading 6'), 'heading')
		self.assertEqual(block_to_block_type('>Q1\n>Q2'), 'quote')

	def test_markdown_to_html(self):
		text = """# This is a heading







	This is a paragraph of text. It has some **bold** and *italic* words inside of it.   

* This is the first list item in a list block
* This is a list item
* This is another list item

1.First
2.Second
3.Third

```
	print('Hello World!')
```

>Four Score
>and Seven years ago
"""
		mdh = markdown_to_html_node(text)
		self.assertEqual(len(mdh), 25)
		self.assertEqual(mdh[0].value, '<div>')
		self.assertEqual(mdh[17].value, '<pre>')
		self.assertEqual(mdh[24].value, '</div>')

	def test_extract_title(self):
		with self.assertRaises(Exception):
			extract_title('Hello World\n\nWill it be found?\n\nNope')
		self.assertEqual(extract_title('Hello World\n\nWill it be found?\n\n#Yes'), 'Yes')
		self.assertEqual(extract_title('Hello World\n\nWill it be found?\n\n# Yes '), 'Yes')
		self.assertEqual(extract_title('Hello World\n\nWill it be found?\n\n# Yes'), 'Yes')

if __name__ == "__main__":
		unittest.main()

