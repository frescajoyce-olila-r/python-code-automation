import scrapy
import requests
from urllib.parse import quote
import json
from urllib.parse import urlparse
from urllib.parse import parse_qs

URL = f'https://www.tekniq.dk/soeg/?pageid=1&section=comp'
API_URL = f'https://newcrm.kundematch.dk//bitrix/components/hvdk/webapi/company.php?method=industry.post'
API_VIP = 'http://api.haandvaerker.dk/supplier/GetVipSupplier'


class TekniqSpider(scrapy.Spider):
    name = 'tekniq'
    allowed_domains = ['tekniq.dk']

    start_urls = [f'{URL}']

    def parse(self, response):
        no_results = response.css('h3.text-header-lg-bold').extract_first()
        current_url = response.request.url
        parsed_url = urlparse(current_url)
        query_params = parse_qs(parsed_url.query)

        if not no_results and 'cvr' in query_params:

            company_name = response.css('h2.text-header-lg-bold::text').extract_first().strip()
            cvr = query_params['cvr'][0]
            telephone = response.css('.underline[href^="tel"]::text').extract_first().strip()
            email = response.css('.text-blue-dark[href^="mailto"]::text').extract_first().strip()
            industry = 'tekniq.dk'
            faglighed = 'tekniq.dk'

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
                "cvr": cvr,
                "telephone": telephone,
                "email": email,
                "industry": industry,
                "Url": response.request.url
            }
        else:
            res = requests.get(API_VIP)
            if res.status_code == 200:
                pretty_json = json.loads(res.text)
                for data in pretty_json:
                    yield scrapy.Request(f'{URL}&cvr={data["CVR"]}', self.parse)
