import json
from scrapy import Spider, Request, FormRequest
from urllib.parse import quote
from pyquery import PyQuery as pq
import requests
import re
import math

BASE_URL = 'http://www.3byggetilbud.dk'
URL = 'http://www.3byggetilbud.dk/leverandoerer'
API_URL = 'https://bitrixapi.haandvaerker.dk/v1/scraper/company?'


class New3byggetilbudSpider(Spider):
    name = '3byggetilbud'

    start_urls = [
        URL + '/adgangskontrol/',
        URL + '/alarminstallatorer-aut/',
        URL + '/algebehandling/',
        URL + '/altaner/',
        URL + '/anlaegsentrepriser/',
        URL + '/badevaerelser/',
        URL + '/blikkenslagere/',
        URL + '/brolaeggere/',
        URL + '/braendeovne/',
        URL + '/byggeradgivning/',
        URL + '/byggematerialer-producenter/',
        URL + '/bygningskonstruktor/',
        URL + '/blowerdoor/',
        URL + '/bygningssagkyndige/',
        URL + '/carportegarager/',
        URL + '/diamantboring/',
        URL + '/diverse/',
        URL + '/dore/',
        URL + '/dortelefonanlaeg/',
        URL + '/drivhuse/',
        URL + '/ejendomsadministration/',
        URL + '/ejendomsmaeglere-statsaut/',
        URL + '/ejendomsservice/',
        URL + '/elevator/',
        URL + '/el-installatorer-aut/',
        URL + '/epoxy-polyurethangulv/',
        URL + '/el-rapport/',
        URL + '/facaderenovering/',
        URL + '/faldstammer/',
        URL + '/finansiering/',
        URL + '/fjernvarme/',
        URL + '/forsikringer/',
        URL + '/flise-og-facaderens/',
        URL + '/fuger/',
        URL + '/glarmestre/',
        URL + '/graffitiafrensning/',
        URL + '/gulvbelaegning/',
        URL + '/haveservice/',
        URL + '/handvaerkerservice/',
        URL + '/husstandsvindmoller/',
        URL + '/havearkitekt/',
        URL + '/indeklima/',
        URL + '/ingeniorer-radg/',
        URL + '/isolering/',
        URL + '/jordvarme/',
        URL + '/jordbundsundersogelser/',
        URL + '/jord-bortkrsel/',
        URL + '/kloakmestre-aut/',
        URL + '/kloakrensning/',
        URL + '/kokkener/',
        URL + '/kloakarbejde/',
        URL + '/legepladsudstyr/',
        URL + '/linoleumvinyl/',
        URL + '/lasesmede/',
        URL + '/malerfirmaer/',
        URL + '/murerfirmaer/',
        URL + '/miljoscreening/',
        URL + '/microcement/',
        URL + '/nedrivning-og-miljsanering/',
        URL + '/nedbrydning-bortskaffelse/',
        URL + '/omfangsdraen/',
        URL + '/porte/',
        URL + '/pillefyr/',
        URL + '/rengoring/',
        URL + '/revisorer/',
        URL + '/radonsikring/',
        URL + '/revisorer-statsaut/',
        URL + '/sandblaesning/',
        URL + '/skadedyrsbekaempelse/',
        URL + '/skimmelsvamp/',
        URL + '/smedefirmaer/',
        URL + '/snedkerfirmaer/',
        URL + '/snerydning/',
        URL + '/tagafrensning/',
        URL + '/tagarbejde/',
        URL + '/tagentrepriser/',
        URL + '/taglejligheder/',
        URL + '/terasser/',
        URL + '/terrazzo/',
        URL + '/tv-inspektion/',
        URL + '/teknisk-isolering/',
        URL + '/udestuer/',
        URL + '/under-og-overstrygning/',
        URL + '/valuarer/',
        URL + '/vedligeholdelsesplaner/',
        URL + '/ventilation/',
        URL + '/vvs-arbejde/',
    ]

    def parse(self, response):
        for href in [pq(x)('a').eq(0).attr('href') for x in pq(response.body)('.results__list > li > a')]:
            yield Request(BASE_URL + href, callback=self.parse_results)

        load_more_btn = pq(response.body)('[class$="__loadmore"]')
        if load_more_btn:
            trade_id = load_more_btn.attr('data-trade_id')
            page = 1
            yield from self.request_next_page(trade_id, page)

    def request_next_page(self, trade_id, page):
        load_more_url = 'https://www.3byggetilbud.dk/wp-admin/admin-ajax.php'
        yield FormRequest(load_more_url, callback=self.parse_load_more, formdata={
            'action': 'get_supplier_list',
            'tradeid': f'{trade_id}',
            'page': f'{page}'
        }, cb_kwargs=dict(trade_id=trade_id))

    def parse_load_more(self, response, trade_id):
        result_data = response.json()['result']['data']
        page_size = result_data['pageSize']
        total = result_data['total'] - page_size
        no_of_pages = math.ceil(total / page_size) + 1
        portals = result_data['data']

        for portal in portals:
            yield Request(portal['portalUrl'], callback=self.parse_results)

        for x in range(2, no_of_pages):
            self.request_next_page(trade_id, x)

    def parse_results(self, response):
        company_name = ''
        cvr = ''
        telephone = ''
        selector = pq(response.body)
        is_competitor = 1
        faglighed = '3byggetilbud.dk'
        industry = '3byggetilbud.dk'

        # first layout check
        if selector('.contractor__title'):
            company_name = selector('.contractor__title').text()
        if selector('.contractor__meta > div'):
            cvr = selector('.contractor__meta > div > span').text()
        if selector('span[itemprop="telephone"]'):
            telephone = selector('span[itemprop="telephone"]').text()

        # second layout check
        if selector('.profile__name'):
            company_name = selector('.profile__name').text()
        if selector('.overview__vat'):
            cvr = re.findall(r'CVR: (\d+)', selector('.overview__vat').text())[0]
        if selector('.overview__phone > span'):
            telephone = selector('.overview__phone > span').text()

        api_url = API_URL
        api_url = f'{api_url}isCompetitor={is_competitor}'
        api_url = f'{api_url}&faglighed={faglighed}'
        api_url = f'{api_url}&industry={industry}'
        api_url = f'{api_url}&companyName={company_name}'
        api_url = f'{api_url}&cvr={cvr}'
        api_url = f'{api_url}&telephone={telephone}'
        api_url = f'{api_url}&url={quote(response.request.url)}'

        print('-------------------------------')
        print(f'Competitor: {is_competitor}')
        print(f'Faglighed: {faglighed}')
        print(f'Industry: {industry}')
        print(f'Company Name : {company_name}')
        print(f'CVR: {cvr}')
        print(f'Telephone: {telephone}')
        print('-------------------------------')


        # Saving data in the API
        res = requests.post(api_url)
        print(f'Saving scraped data in api...')
        print(response.url)
        print(res.status_code)

        if res.status_code == 201:
            pretty_json = json.loads(res.text)
            print(json.dumps(pretty_json, indent=2))
