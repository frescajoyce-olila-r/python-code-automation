import scrapy
import requests
from urllib.parse import quote
import json
import urllib.parse


URL = f'https://enrigtigmaler.dk/umbraco/api/search/getmalermestrebymemberinfo?query='
API_URL = f'https://newcrm.kundematch.dk//bitrix/components/hvdk/webapi/company.php?method=industry.post'


class EnrigtigmalerSpider(scrapy.Spider):
    name = 'enrigtigmaler'
    allowed_domains = ['enrigtigmaler.dk']

    start_urls = [URL]

    def parse(self, response):
        pretty_json = json.loads(response.body)
        industry = 'enrigtigmaler.dk'
        faglighed = 'enrigtigmaler.dk'
        for data in pretty_json:
            company_name = data.get('CompanyName')
            cvr = data.get('Cvr')
            telephone = data.get('Phone')
            email = data.get('Email')

            api_url = API_URL

            if company_name:
                api_url += f'&companyName={company_name}'
            if cvr:
                api_url += f'&cvr={cvr}'
            if telephone:
                api_url += f'&telephone={telephone}'
            if email:
                api_url += f'&email={email}'
            if industry:
                api_url += f'&industry={industry}'
            if faglighed:
                api_url += f'&faglighed={faglighed}'

            if api_url:
                api_url += f'&url={quote(response.request.url)}'

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
                "Cvr": cvr,
                "Mobile": telephone,
                "Email": email,
                "industry": industry,
                "Url": response.request.url
            }