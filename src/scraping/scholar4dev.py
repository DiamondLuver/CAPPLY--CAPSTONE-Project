# deadline problem

import requests
from bs4 import BeautifulSoup
import sqlite3, string, random
from django.utils.text import slugify


def random_slug():
    allowed_chars = ''.join((string.ascii_letters, string.digits))
    unique_slug = ''.join(random.choice(allowed_chars) for _ in range(32))
    return unique_slug


conn = sqlite3.connect('src/db.sqlite3')
c = conn.cursor()

for i in range (1, 3):
    web_link = f'https://www.scholars4dev.com/page/{i}/'
    r = requests.get(web_link)
    soup = BeautifulSoup(r.content, 'lxml')

    lists = soup.find_all('div', id = 'contentleft')
    for list in lists:
        listing = list.find_all('div', class_ = 'entry clearfix')
        for info in listing:
            more_info = info.find('h2').a['href']
            school = info.find('h2').text

            country = info.find(string=lambda text: 'study' in text.lower())
            if country:
                country = country.text.strip().split(':')[-1].strip()
            
            level = info.find(string=lambda text: 'degree' in text.lower())
            if level:
                level = level.text.strip()
            else:
                level = more_info
                
            deadline = info.find(string=lambda text: '2023' in text.lower())
            if deadline:
                deadline = deadline.text
            else:
                deadline = web_link
            slug_combine = school + " " + random_slug()
            slug = slugify(slug_combine)
            print(deadline)
            c.execute('''INSERT INTO category_scholarship VALUES(?,?,?,?,?,?,?,?,?)''',(None, level, school, deadline, more_info,None, web_link, country, slug))
                
            # c.execute('''INSERT INTO category_scholarship VALUES(?,?,?,?,?,?,?,?,?)''',(None, level, school, deadline, more_info, None , web_link, country, slug))
              
conn.commit()
print('complete.')

#close connection
conn.close()

            