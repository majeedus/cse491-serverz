# __init__.py is the top level file in a Python package.
import sqlite3
import os
from quixote.publish import Publisher

# this imports the class RootDirectory from the file 'root.py'
from .root import RootDirectory
from . import html, image

def create_publisher():
     p = Publisher(RootDirectory(), display_exceptions='plain')
     p.is_thread_safe = True
     return p
 
def setup():                            # stuff that should be run once.
    html.init_templates()
	#sqllite implementation 
	if not os.path.exists('./db.sqlite3'):
		db = sqlite3.connect('db.sqlite3')
		db.execute('CREATE TABLE IF NOT EXISTS image_store' + 
					'(i INTEGER PRIMARY KEY, image BLOB, type TEXT,' + 
	    			'name TEXT, description TEXT)')
	
    some_data = open('imageapp/dice.png', 'rb').read()
    image.add_image(some_data)
    

def teardown():                         # stuff that should be run once.
    pass
