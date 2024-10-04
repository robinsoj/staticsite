from leafnode import LeafNode
from htmlnode import HTMLNode
from textnode import TextNode
import re

def extract_markdown_images(text):
	alt_matches = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
	return alt_matches

def extract_markdown_links(text):
	url_matches = re.findall(r"(?<!!)\[(.*?)\]\((.*?)\)", text)
	return url_matches


