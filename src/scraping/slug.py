import random
import string
import requests
from bs4 import BeautifulSoup 
import sqlite3
from django.utils.text import slugify

# conn = sqlite3.connect('src/db.sqlite3')
# c = conn.cursor()

def random_slug():
    allowed_chars = ''.join((string.ascii_letters, string.digits))
    unique_slug = ''.join(random.choice(allowed_chars) for _ in range(32))
    return unique_slug

# for i in range (1, 3):
#     web_link = f'https://www.scholars4dev.com/page/{i}/'
#     r = requests.get(web_link)
#     soup = BeautifulSoup(r.content, 'lxml')

# level= "Test"
# school = "Test of school"
# deadline = "Test"
# more_info = "test"
# country = "test"
# slug_combine = school + random_slug()
# slug = slugify(slug_combine)
# c.execute('''INSERT INTO category_scholarship VALUES(?,?,?,?,?,?,?,?,?)''',(None, level, school, deadline, more_info,None, web_link, country, slug))
              
# conn.commit()
# print('complete.')

# #close connection
# conn.close()

            