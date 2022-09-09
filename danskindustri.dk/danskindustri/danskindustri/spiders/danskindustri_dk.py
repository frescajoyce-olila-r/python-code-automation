import scrapy
import requests
from urllib.parse import quote
import json
import urllib.parse

ZIP_FROM = 1000
ZIP_TO = 9999

#URL = f'https://www.danskindustri.dk/brancher/di-byggeri/find-medlemmer/?zipFrom={ZIP_FROM}&zipTo={ZIP_TO}&Page=1'
URL = f'https://www.danskindustri.dk/brancher/di-byggeri/find-medlemmer/?SearchQuery=&zipFrom=1000&zipTo=9999&profession=V%C3%A6lg%20faglighed'
API_URL = f'https://newcrm.kundematch.dk//bitrix/components/hvdk/webapi/company.php?method=industry.post'
API_VIP = 'http://api.haandvaerker.dk/supplier/GetVipSupplier'

PROFESSIONS = {
    'Vælg faglighed':'Vælg faglighed',                                                 # Vælg faglighed
    'Tag og facade':'123,124,128,103,101,114,116,102',                                 # Tag og facade
    'Tømrer og snedker': '123,124,108,125,114,121,116,102',                            # Tømrer og snedker
    'Materieludlejning': '111,115',                                                    # Materieludlejning
    'Industriel produktion': '120,1111,1112,1113,108,107,104,109',                     # Industriel produktion
    'Anlægsarbejde': '119,105,128,108,110,126,129,122,117',                            # Anlægsarbejde
    'Murer': '124,108,101,114,122,116',                                                # Murer
    'Maler': '124,108,103,114',                                                        # Maler
    'Miljø og nedrivning': '113,112',                                                  # Miljø og nedrivning
}

LOADED_PROFESSIONS = ['Vælg faglighed']


class DanskindustriSpider(scrapy.Spider):
    name = 'danskindustri'
    allowed_domains = ['danskindustri.dk']

    start_urls = [f'{URL}&profession={PROFESSIONS[LOADED_PROFESSIONS[-1]]}']

    def parse(self, response):

        for list_item in response.css('.abstract-list__item.abstract-list__item--no-image'):
            fields = list_item.css('.organisation-info__item')
            company_name = list_item.css('.abstract-list__item__content__head::text').extract_first().strip()
            cvr = ''
            telephone = ''
            email = ''
            industry = 'danskindustri.dk'

            for field in fields:
                label = field.css('.label::text').extract_first().strip()
                value = ', '.join(field.css('.value::text').extract())

                if label == 'CVR-nr:':
                    cvr = value
                elif label == 'Telefon:':
                    telephone = value
                elif label == 'E-mail:':
                    email = value
                elif label == 'Industry:':
                    industry = value

            api_url = f'{API_URL}&faglighed={LOADED_PROFESSIONS[-1]}'
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
                "cvr": cvr,
                "telephone": telephone,
                "email": email,
                "industry": industry,
                "Url" : response.request.url

            }

        next_page = response.css('.paging > .paging__list > li:last-child > a:first-child::attr(href)').extract_first()
        if next_page:
            yield scrapy.Request(response.urljoin(next_page), self.parse)
        else:
            temp = list(PROFESSIONS)
            next_profession = temp[temp.index(PROFESSIONS[-1]) + 1]
            print(f'Next Profession: {next_profession}')
            if next_profession:
                print(f'Next URL: {URL}&profession={next_profession}')
                LOADED_PROFESSIONS.append(next_profession)
                yield scrapy.Request(f'{URL}&profession={next_profession}', self.parse)

            else:
                res = requests.get(API_VIP)
                if res.status_code == 200:
                    pretty_json = json.loads(res.text)
                    for data in pretty_json:
                        yield scrapy.Request(f'{URL}&SearchQuery={data["CVR"]}', self.parse)