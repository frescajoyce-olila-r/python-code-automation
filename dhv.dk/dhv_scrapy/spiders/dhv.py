import scrapy
import requests
from urllib.parse import quote
import json

url = f'https://dhv.dk/haandvaerkerliste/'
API_URL = f'https://newcrm.kundematch.dk//bitrix/components/hvdk/webapi/company.php?method=industry.post'

class DHVSpider(scrapy.Spider):
    name = 'dhv'
    allowed_domains = ['dhv.dk']

    start_urls = [url]

    def parse(self, response):
        industry = 'dhv.dk'
        faglighed = 'dhv.dk'
        for list_item in response.css('#the-list tr'):
            fields = list_item.css('td')
            company_name = ''
            cvr = ''
            telephone = ''
            email = ''

            api_url = API_URL

            for field in fields:
                class_name = field.xpath('@class').extract_first().split(' ')[0]
                value = field.css('::text').extract_first()
                if value:
                    value = value.strip()

                if class_name == 'company_name':
                    company_name = value
                if class_name == 'CVR._Nr.':
                    cvr = value
                if class_name == 'tlf._nr.':
                    telephone = value
                if class_name == 'email':
                    email = value

            if company_name:
                api_url += f'&companyName={quote(company_name)}'
            if cvr:
                api_url += f'&cvr={quote(cvr)}'
            if telephone:
                api_url += f'&telephone={telephone}'
            if email:
                api_url += f'&email={quote(email)}'
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
            print(f'Fagligheg: {faglighed}')
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
                "Url" : response.request.url
            }

        next_page = response.css('.next-page::attr(href)').extract_first()
        if next_page:
            yield scrapy.Request(response.urljoin(next_page), self.parse)