import requests
from bs4 import BeautifulSoup
import boto3
import csv
import datetime
import dateutil.tz


def f1(event, context):
	s3 = boto3.client('s3')
	tiempo_file()
	publimetro_file()
	eastern = dateutil.tz.gettz('US/Eastern')
	date = datetime.datetime.now(tz=eastern)
	s3.upload_file(f'/tmp/headline_eltiempo.csv', 'bigdata981110-2', f'headlines/final/periodico=eltiempo/year={date.year}/month={date.month}/day={date.day}/headline.csv')
	s3.upload_file(f'/tmp/headline_publimetro.csv', 'bigdata981110-2', f'headlines/final/periodico=publimetro/year={date.year}/month={date.month}/day={date.day}/headline.csv')


def tiempo_file():
	r = requests.get('https://www.eltiempo.com')
	soup = BeautifulSoup(r.text, 'lxml')


	articles = soup.find_all('article')

	with open('/tmp/headline_eltiempo.csv', 'w', newline='') as file:
		writer = csv.writer(file)
		index = 1
		for article in articles:
				if(article != None):

					title = ''
					category = ''
					headline_link = ''

					title_tag = article.find('a', class_='title page-link')
					if title_tag != None:
							title = title_tag.text
							headline_link = title_tag['href']
					else:
						continue
					
					category_tag = article.find('a', class_='category')
					if category_tag != None:
							category = category_tag.text
					else:
						continue
					
						
	
					writer.writerow([title, category, headline_link])
					download_news(f'https://www.eltiempo.com{headline_link}', 'eltiempo', index)
					index += 1

def publimetro_file():
	r = requests.get('https://www.publimetro.co/co/')
	soup = BeautifulSoup(r.text, 'lxml')

	data = []

	articles = soup.find_all('div', class_='MuiCardContent-root')
	index = 1
	for art in articles:
	    title = ''
	    category = ''
	    headline_link = ''

	    if art.a != None:
	            headline_link = art.a['href']
	            if art.a.h2 != None:
	                title = art.a.h2.text
	            else:
	                continue
	    else:
	        continue

	    if art != None:
	        if art.h6 != None:
	            category = art.h6.text
	        else:
	            continue
	    else:
	        continue

        
	    data.append([title, category, headline_link])
		if headline_link[:3] == 'http':
			download_news(f'{headline_link}', 'publimetro', index)
		else:
			download_news(f'https://www.publimetro.co{headline_link}', 'publimetro', index)
		index += 1
    
	more_articles = soup.find_all('div', class_='jss81')
	for art in more_articles:

	    title = ''
	    category = ''
	    headline_link = ''

            
	    if art != None:

	        if art.a != None:
	            headline_link = art.a['href']
	            if art.a.h1 != None:
	                title = art.a.h1.text
	            else:
	                continue
	        else:
	            continue

	        if art.h6 != None:
	            if art.h6.text:
	                category = art.h6.text
	            else:
	                continue
	        else:
	            continue
	    else:
	        continue
        
	    data.append([title, category, headline_link])
		if headline_link[:3] == 'http':
			download_news(f'{headline_link}', 'publimetro', index)
		else:
			download_news(f'https://www.publimetro.co{headline_link}', 'publimetro', index)
		index += 1
        
	
	with open('/tmp/headline_publimetro.csv', 'w', newline='') as file:
		writer = csv.writer(file)
		writer.writerows(data)

    
def download_news(url, periodico, index):
	s3 = boto3.client('s3')
	

	r = requests.get(url)
	open(f'/tmp/page_{index}.html', 'wb').write(r.content)


	eastern = dateutil.tz.gettz('US/Eastern')
	date = datetime.datetime.now(tz=eastern)
	s3.upload_file(f'/tmp/page_{index}.html', 'bigdata981110-2', f'news/raw/periodico={periodico}/year={date.year}/month={date.month}/day={date.day}/{index}.html')
