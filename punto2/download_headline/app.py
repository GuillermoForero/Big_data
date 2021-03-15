import requests
from bs4 import BeautifulSoup
import boto3
import csv
import datetime
import dateutil.tz


def f1(event, context):
	s3 = boto3.client('s3')
	

	r_eltiempo = requests.get('https://www.eltiempo.com/')
	open('/tmp/page_eltiempo.html', 'wb').write(r_eltiempo.content)

	r_publimetro = requests.get('https://www.publimetro.co/co/')
	open('/tmp/page_publimetro.html', 'wb').write(r_publimetro.content)

	eastern = dateutil.tz.gettz('US/Eastern')
	date = datetime.datetime.now(tz=eastern)
	s3.upload_file(f'/tmp/page_eltiempo.html', 'bigdata981110-2', f'headlines/raw/periodico=eltiempo/year={date.year}/month={date.month}/day={date.day}/page.html')
	s3.upload_file(f'/tmp/page_publimetro.html', 'bigdata981110-2', f'headlines/raw/periodico=publimetro/year={date.year}/month={date.month}/day={date.day}/page.html')


