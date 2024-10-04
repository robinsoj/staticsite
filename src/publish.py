import os
import os.path
import shutil

def purge_directory(dir):
	print(dir)
	if os.path.exists(dir) == False:
		return None
	entries = os.listdir(dir)
	for item in entries:
		full_path = os.path.join(dir, item)
		if os.path.isdir(full_path):
			purge_directory(full_path)

	print('delete', dir)
	shutil.rmtree(dir)

def copy_directory(dir, target):
	print(dir, target)
	if os.path.exists(dir) == False:
		return None
	entries = os.listdir(dir)
	for item in entries:
		full_path = os.path.join(dir, item)
		target_path = os.path.join(target, item)
		if os.path.isdir(full_path):
			os.mkdir(target_path)
			copy_directory(full_path, target_path)
		else:
			print('copying', full_path, 'to', target_path)
			shutil.copy(full_path, target_path)
	 
if __name__ == '__main__':
	purge_directory('.\\public')
	os.mkdir('.\\public')
	copy_directory('.\\static', '.\\public')
