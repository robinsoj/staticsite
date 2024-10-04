from split_nodes_delimiter import *
from publish import *

def main():
	purge_directory('./public')
	os.mkdir('./public')
	copy_directory('./static', './public')
	generate_pages_recursive('./content', './template.html', './public')

main()
