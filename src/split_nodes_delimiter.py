from textnode import TextNode
from collections import Counter
from extract_images import *
from text_node_to_html_node import *
import re
import os
import os.path
import shutil
from pathlib import Path

def split_nodes_delimiter(old_nodes, delimiter, text_type):
	ret_list = []
	for node in old_nodes:
		node_text = node.text
		counter = Counter(node_text)
		if (counter[delimiter] % 2 != 0):
			raise Exception(f"Closing delimiter {delimiter} not found")
		texts = node_text.split(delimiter)
		old_format = True
		for text in texts:
			if old_format:
				ret_list.append(TextNode(f"{text}", node.text_type))
				old_format = False
			else:
				ret_list.append(TextNode(text, text_type))
				old_format = True
	return ret_list

def split_nodes_image(old_nodes):
	new_nodes = []
	for old_node in old_nodes:
		if old_node.text_type != 'text':
			new_nodes.append(old_node)
			continue
		original_text = old_node.text
		images = extract_markdown_images(original_text)
		if len(images) == 0:
			new_nodes.append(old_node)
			continue
		for image in images:
			sections = original_text.split(f"![{image[0]}]({image[1]})", 1)
			if len(sections) != 2:
				raise ValueError("Invalid markdown, image section not closed")
			if sections[0] != "":
				new_nodes.append(TextNode(sections[0], 'text'))
			new_nodes.append(
				TextNode(
					image[0],
					'image',
					image[1],
				)
			)
			original_text = sections[1]
		if original_text != "":
			new_nodes.append(TextNode(original_text, 'text'))
	return new_nodes
	

def split_nodes_link(old_nodes):
	new_nodes = []
	for old_node in old_nodes:
		if old_node.text_type != 'text':
			new_nodes.append(old_node)
			continue
		original_text = old_node.text
		links = extract_markdown_links(original_text)
		if len(links) == 0:
			new_nodes.append(old_node)
			continue
		for link in links:
			sections = original_text.split(f"[{link[0]}]({link[1]})", 1)
			if len(sections) != 2:
				raise ValueError("Invalid markdown, link section not closed")
			if sections[0] != "":
				new_nodes.append(TextNode(sections[0], 'text'))
			new_nodes.append(TextNode(link[0], 'link', link[1]))
			original_text = sections[1]
		if original_text != "":
			new_nodes.append(TextNode(original_text, 'text'))
	return new_nodes

def text_to_textnode(text):
	ret_list = []
	nodes = split_nodes_delimiter([TextNode(text, 'text')], '**', 'bold')
	nodes = split_nodes_delimiter(nodes, '*', 'italic')
	nodes = split_nodes_delimiter(nodes, '`', 'code')
	new_nodes = []
	for node in nodes:
		new_nodes.extend(split_nodes_image([node]))
	nodes = new_nodes;
	new_nodes = []
	for node in nodes:
		new_nodes.extend(split_nodes_link([node]))
	nodes = new_nodes
	return nodes

def markdown_to_blocks(markdown):
	ret_list = []
	re_markdown = re.sub(r'\n{2,}', '\n\n', markdown)
	hold_markdown = re_markdown.split('\n\n')
	for md in hold_markdown:
		ret_list.extend([md.lstrip().rstrip()])
	return ret_list

def block_to_block_type(block):
	heading = (re.match('^#{1,6} ', block) is not None)
	code_block = (re.match(r'^```[\s\S]*```$', block, re.DOTALL) is not None)
	lines = block.split('\n')
	quote = True
	order_list = True
	unorder_list = True
	i = 1
	for line in lines:
		quote = quote and (line[0] == '>')
		order_list = order_list and (re.match(rf'^{i}\.', line) is not None)
		unorder_list = unorder_list and (line[:2] in ['* ', '- '])
		i += 1
	if heading:
		return 'heading'
	elif code_block:
		return 'code'
	elif quote:
		return 'quote'
	elif order_list:
		return 'ordered list'
	elif unorder_list:
		return 'unordered list'
	return 'paragraph'

def text_to_header(text):
	i = 0
	new_text = text
	while (new_text[0] == '#') and (i < 6):
		new_text = new_text[1:]
		i += 1
	new_text = new_text.lstrip().rstrip()
	ret_text = text_node_to_html_node(TextNode(f'<h{i}>{new_text}</h{i}>', 'text'))
	return [ret_text]

def text_to_code(text):
	new_text = re.search(r'^```([\s\S]*)```$', text, re.DOTALL).group(1)
	ret_list = [text_node_to_html_node(TextNode('<pre>', 'text'))]
	ret_list.extend([text_node_to_html_node(TextNode(new_text, 'code'))])
	ret_list.extend([text_node_to_html_node(TextNode('</pre>', 'text'))])
	return ret_list

def text_to_quote(text):
	new_text = text.split('\n')
	ret_list = [text_node_to_html_node(TextNode('<blockquote>', 'text'))]
	for txt in new_text:
		txt = txt[1:].lstrip().rstrip()
		ret_list.extend([text_node_to_html_node(TextNode(txt, 'text'))])
	ret_list.extend([text_node_to_html_node(TextNode('</blockquote>', 'text'))])
	return ret_list

def text_to_ol(text):
	new_text = text.split('\n')
	ret_list = [text_node_to_html_node(TextNode('<ol>', 'text'))]
	for txt in new_text:
		txt = txt[2:].lstrip().rstrip()
		nodes = text_to_textnode('<li>'+txt+'</li>')
		for node in nodes:
			ret_list.extend([text_node_to_html_node(node)])
	ret_list.extend([text_node_to_html_node(TextNode('</ol>', 'text'))])
	return ret_list

def text_to_ul(text):
	new_text = text.split('\n')
	ret_list = [text_node_to_html_node(TextNode('<ul>', 'text'))]
	for txt in new_text:
		txt = txt[2:].lstrip().rstrip()
		nodes = text_to_textnode('<li>'+txt+'</li>')
		for node in nodes:
			ret_list.extend([text_node_to_html_node(node)])
	ret_list.extend([text_node_to_html_node(TextNode('</ul>', 'text'))])
	return ret_list

def text_to_paragraph(text):
	new_text = text.split('\n')
	ret_list = []
	for txt in new_text:
		nodes = text_to_textnode(txt)
		for node in nodes:
			ret_list.extend([text_node_to_html_node(node)])
	return ret_list

def text_to_children(block):
	match(block_to_block_type(block)):
		case 'heading':
			node = text_to_header(block)
		case 'code':
			node = text_to_code(block)
		case 'quote':
			node = text_to_quote(block)
		case 'ordered list':
			node = text_to_ol(block)
		case 'unordered list':
			node = text_to_ul(block)
		case _:
			node = text_to_paragraph(block)
	return node

def markdown_to_html_node(markdown):
	ret_list = [text_node_to_html_node(TextNode('<div>', 'text'))]
	blocks = markdown_to_blocks(markdown)
	for block in blocks:
		ret_list.extend(text_to_children(block))

	ret_list.extend([text_node_to_html_node(TextNode('</div>', 'text'))])
	return ret_list

def extract_title(markdown):
	h1_found = False
	ret_text = ''
	markdown_lines = markdown.split('\n')
	for mdl in markdown_lines:
		if (re.match(r'^#[^#]', mdl) is not None):
			hl_found = True
			ret_text = mdl[1:].lstrip().rstrip()
	if not hl_found:
		raise Except('Header 1 not found in markdown')
	return ret_text

def generate_page(from_path, template_path, dest_path):
	print(f"Generating page from {from_path} to {dest_path} using {template_path}")
	fr_file = open(from_path, 'r')
	fr_file_contents = fr_file.read()
	fr_file.close()

	tmp_file = open(template_path, 'r')
	tmp_file_contents = tmp_file.read()
	tmp_file.close()

	html_nodes = markdown_to_html_node(fr_file_contents)
	html_text = ''
	for html_node in html_nodes:
		html_text += html_node.to_html()

	title = extract_title(fr_file_contents)
	html_page = tmp_file_contents.replace('{{ Title }}', title).replace('{{ Content }}', html_text)

	dir_name = os.path.dirname(dest_path)
	if dir_name != '':
		os.makedirs(dir_name, exist_ok=True)
	to_file = open(dest_path, 'w')
	to_file.write(html_page)
	to_file.close()

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
	for filename in os.listdir(dir_path_content):
		from_path = os.path.join(dir_path_content, filename)
		dest_path = os.path.join(dest_dir_path, filename)
		if os.path.isfile(from_path):
			dest_path = Path(dest_path).with_suffix(".html")
			generate_page(from_path, template_path, dest_path)
		else:
			generate_pages_recursive(from_path, template_path, dest_path)