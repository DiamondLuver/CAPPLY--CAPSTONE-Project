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

for i in range(1, 20):
    link_web = f'https://www.wedushare.com/all-program?short_by=All&page={i}'
    r = requests.get(link_web)
    soup = BeautifulSoup(r.content, 'lxml')
    lists = soup.find_all('div', class_ = 'article-list grid-2 mb-2')
    for list in lists:
        listing = list.find_all('div', class_ = 'item shadow--hover')
        for link in listing:
            school = link.find('a', class_ = 'text-default text-sub sub-2').text.strip()
            more_info = link.find('a', class_ = 'text-default text-sub sub-2').get('href').strip()
            deadline = link.find('span').text.strip().split(':')[-1].strip()
            countries = link.find('div', class_ = 'col')
            country = countries.span.text.strip()
            level = link.find_all('span', class_ = 'text-muted text-sm')[1].text.strip()
            study_field = 'option'

            
            slug_combine = school + " " + random_slug()
            slug = slugify(slug_combine)
            c.execute('''INSERT INTO category_scholarship VALUES(?,?,?,?,?,?,?,?,?)''',(None, level, school, deadline, more_info, None, link_web, country, slug))
           
            # c.execute('''INSERT INTO category_scholarship VALUES(?,?,?,?,?,?,?,?,?)''',(None, level, school, deadline,more_info,None, link_web, country, None))

conn.commit()
print('complete.')

#close connection
conn.close()