import requests
from bs4 import BeautifulSoup
import string, random
from django.utils.text import slugify
from django.http import JsonResponse



def random_slug():
    allowed_chars = ''.join((string.ascii_letters, string.digits))
    unique_slug = ''.join(random.choice(allowed_chars) for _ in range(32))
    return unique_slug
def scrape_data(request):
    results = []  # List to store the scraped objects
    
    for i in range(1, 3):
        web_link = f'https://www.idp.com/cambodia/search/scholarship/?studyLevel=%3Aundergraduate&page={i}'
        r = requests.get(web_link)
        soup = BeautifulSoup(r.content, 'lxml')
        lists = soup.find_all('div', class_='pro_wrap')
        
        for lst in lists:
            listing = lst.find_all('div', class_='pro_list_wrap')
            
            for info in listing:
                link = info.find('a', class_='prdct_lnk').get('href')
                more_info = 'https://www.idp.com' + link
                schools = info.find('div', class_='ins_cnt')
                school = schools.a.text.strip()
                country = schools.p.text.strip().split(',')[-1].strip()
                level = info.find('div', class_='media_txt').text.strip().split('Qualification')[-1].strip()
                deadline = 'more'
                allowed_chars = ''.join((string.ascii_letters, string.digits))
                slug_combine = school + " " + ''.join(random.choice(allowed_chars) for _ in range(32))
                slug = slugify(slug_combine)
                
                # Create an object or dictionary to store the scraped data
                obj = {
                    'more_info': more_info,
                    'school': school,
                    'country': country,
                    'level': level,
                    'deadline': deadline,
                    'slug': slug
                }
                
                results.append(obj)  # Append the object to the results list
    
    return JsonResponse(results, safe=False)
