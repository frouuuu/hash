import sqlite3
import hashlib
import os
import sys

''' global variables '''

conn = sqlite3.connect('/home/iwona/gapa.db') 
conn.text_factory = str
c = conn.cursor()
path = 'none'
tbl_name = 'none' 
file_ls = []

''' functions '''

def path():
	global path
	path = raw_input("Select directory: ")
	while os.path.exists(path) == False:
		print "Directory does not exist. Select directory or 'exit'"
		path = raw_input("Select directory: ")
		if path.lower() == 'exit':
			sys.exit()

def create_table_hash(path):
	global tbl_name
	list_path = path.split('/')
	list_len = len(list_path)
	tbl_name = list_path[list_len -1] 
	tbl_name = tbl_name.replace(" ", "_")
	c.execute("CREATE TABLE if not exists %s (file_name varchar(255), hash_value varchar(255), modified_hash varchar(1));" %tbl_name)
	conn.commit()
	
def add_hashes_to_table(path, tbl_name):
	global file_ls
	c.execute('SELECT file_name FROM %s;' %tbl_name)
	tbl_name_list = c.fetchall() 
	file_ls = os.listdir(path) 
	tbl_dict = {}
	for i in tbl_name_list:
		temp = c.execute("SELECT hash_value FROM %s WHERE file_name = '%s';" %(tbl_name, i[0]))
		temp = temp.fetchone()
		tbl_dict[i[0]] = temp[0]
	
	for item in file_ls:
		item = item.replace(" ", "_")
		hash_item = hashlib.md5(item)
		h = hash_item.hexdigest()
		if item in tbl_dict.keys():
			if h == tbl_dict.get(item, ''):
				c.execute("UPDATE %s SET  modified_hash = 'N' WHERE file_name = '%s';" % (tbl_name, item ))
				conn.commit()
			else:
				c.execute("UPDATE %s SET hash_value = '%s', modified_hash = 'Y' WHERE file_name = '%s';" % (tbl_name, h, item ))
				conn.commit()
		else:
			c.execute("INSERT INTO %s (file_name, hash_value, modified_hash) VALUES ('%s', '%s', 'N');" % (tbl_name, item, h))
			print 'ADDED' + item + ' ' + h
			conn.commit()
			
'''body'''

path()
create_table_hash(path)
add_hashes_to_table(path, tbl_name)




	
