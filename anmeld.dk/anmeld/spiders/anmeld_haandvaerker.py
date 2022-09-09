from scrapy import Spider, Request
from pyquery import PyQuery as pq
from urllib.parse import quote
import requests
import json


class AnmeldSpiderSpider(Spider):
    name = 'anmeld_haandvaerker'

    def __init__(self, *args, **kwargs):

        self.start_urls = [f'https://www.anmeld-haandvaerker.dk/resultater?search=&page={x}' for x in range(0,12844)]

    def parse(self, response):
        for part in [['https://www.anmeld-haandvaerker.dk'+pq(x)('a.btn.btn-black').eq(0).attr('href'),pq(x)('.ratingcount').text().replace(" anmeldelser","") ] for x in pq(response.body)('.craftsman-profile') if pq(x)('a.btn.btn-black').eq(0).attr('href')!=None]:
            if int(part[1])>0:
                yield Request(part[0], callback=self.parse_profiles)

    def parse_profiles(self, response):
        selector = pq(response.body)
        api_url = 'https://bitrixapi.haandvaerker.dk/v1/scraper/company?'
        api_url += f'url={quote(response.url)}' # url
        api_url += f'&isCompetitor=1' # isCompetitor
        api_url += f'&faglighed=anmeld-haandvaerker.dk' # faglighed
        api_url += f'&industry=anmeld-haandvaerker.dk' # industry
        api_url += f'&companyName=anmeld' # companyName

        if selector(".hero-img").attr("class").find("not-member")==-1:
            api_url += f'&cvr={selector(".cvr_link").eq(0).text()}' # cvr
            api_url += f'&telephone={selector(".ex-bold").parents(".info").eq(0).text().replace("Telefon: ", "")}' # telephone
            api_url += f'&firstMemberYear={selector(".member_since").eq(0).text()}' # firstMemberYear

            print(f'Saving scraped data in api...')
            res = requests.post(api_url)
            print(response.url)

            if res.status_code == 201:
                pretty_json = json.loads(res.text)
                print(json.dumps(pretty_json, indent=2))