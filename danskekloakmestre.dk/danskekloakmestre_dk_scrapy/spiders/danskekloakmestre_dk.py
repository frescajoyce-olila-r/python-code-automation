import re

import scrapy
import requests
from urllib.parse import quote
import json
import urllib.parse


URL = f'https://www.danskekloakmestre.dk/private/find-kloakmester'
API_URL = f'https://newcrm.kundematch.dk//bitrix/components/hvdk/webapi/company.php?method=industry.post'
API_VIP = 'http://api.haandvaerker.dk/supplier/GetVipSupplier'


class DanskekloakmestreSpider(scrapy.Spider):
    name = 'danskekloakmestre'
    allowed_domains = ['danskekloakmestre.dk']

    start_urls = [f'{URL}']
    def parse(self, response):
        source = response.text
        companies = re.findall(r'<b>(.+?)</b>', source)
        cvrs = re.findall(r'<td class=\'country\-name\'>CVR\.nr\.: (.+?)</td>', source)
        telephones = re.findall(r'<td class=\'country\-name\'>Telefon: (.+?)</td>', source)
        emails = re.findall(r'<a href=\'mailto:.*?\'>(.+?)</a>', source)

        for index, value in enumerate(companies):
            company_name = value
            cvr = cvrs[index].replace(' ', '')
            telephone = telephones[index]
            email = emails[index]
            industry = 'danskekloakmestre.dk'
            faglighed = 'danskekloakmestre.dk'

            api_url = f'{API_URL}&faglighed={faglighed}&industry={industry}'
            if company_name:
                api_url += f'&companyName={company_name}'
            if cvr:
                api_url += f'&cvr={cvr}'
            if telephone:
                api_url += f'&telephone={telephone}'
            if email:
                api_url += f'&email={email}'

            if api_url:
                api_url+= f'&url={quote(response.request.url)}'

            print('Summary of web scraping: \n')
            print(f'Status Response: {response}')
            print(f'Company Name: {company_name}')
            print(f'CVR: {cvr}')
            print(f'Telephone: {telephone}')
            print(f'Email: {email}')
            print(f'Industry: {industry}')
            print(f'URL: {response.request.url}\n')

            print(f'Saving scraped data in api...')
            res = requests.get(api_url)

            if res.status_code == 200:
                pretty_json = json.loads(res.text)
                print(json.dumps(pretty_json, indent=2))

            yield {
                "companyName": company_name,
                "cvr": cvr.strip(),
                "telephone": telephone,
                "email": email,
                "industry": industry,
                "Url": response.request.url
            }
