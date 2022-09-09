import re
from scrapy.http import JsonRequest
from scrapy import Spider, Request
from pyquery import PyQuery as pq
import requests

class AnmeldSpiderSpider(Spider):
    name = 'byggetilbud'

    def __init__(self, *args, **kwargs):
        self.start_urls = ['https://www.byggetilbud.dk/trust/']

    def parse(self, response, **kwargs):
        selector = pq(response.body)
        Links = ['https://www.byggetilbud.dk' + pq(x).attr('href') for x in selector('[style="color:#000;text-decoration:underline;"]')]
        for Link in Links:
            yield Request(Link, callback=self.parse_categories)

    def parse_categories(self, response):

        selector = pq(response.body)
        try:
            last_page = int(selector('.pagination li').eq(-1).text())
        except:
            last_page = 1
        Links = [f'{response.url}?page={x}' for x in range(1,last_page+1)]
        for Link in Links:
            yield Request(Link, callback=self.parse_categories_pages)

    def parse_categories_pages(self, response):
        selector = pq(response.body)
        Links = selector('.item_company_block')
        for pre_select in Links:
            sub_select = pq(pre_select)
            if sub_select.attr('data-href').find('http')==-1:
                Link = 'https://www.byggetilbud.dk' + sub_select.attr('data-href')
            else:
                Link = sub_select.attr('data-href')
            yield Request(Link, callback=self.parse_profiles)

    def parse_profiles(self, response):
        selector = pq(response.body)
        id_ = selector("[data-companyid]").eq(0).attr("data-companyid")
        item={}
        item["URL"]=response.url
        item["NUMBER_OF_REVIEWS"]= re.findall(r'(\d+)', selector(".company-info div> span").eq(1).text())[0]
        item["COMPANY_NAME"]=selector(".company_name").text()
        try:
            item["CVR_NO"]=re.findall(r'CVR (\d+)', selector('.row-fluid p:contains("CVR")').text())[0]
        except:
            item["CVR_NO"] = ''
        try:
            headers = {'Accept': 'application/json, text/javascript, */*; q=0.01','X-Requested-With': 'XMLHttpRequest',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36'}
            url = f'https://www.byggetilbud.dk/ajax/firma/load_reviews'
            last_page = requests.post(url,headers=headers, data={'company_id': id_,'page': '1','comment': '0',}).json()['asd']

            for page in range(1,last_page+1):
                HTML  = requests.post(url,headers=headers, data={'company_id': id_,'page': page,'comment': '0',}).json()['html']
                selector = pq(HTML)
                for review in selector('.review'):
                    sub_selector = pq(review)
                    item['REVIEW_RATING']=sub_selector('.new_stars_block_20').attr('title').replace("/5","")
                    item['REVIEW_DATE']=sub_selector('.block_review_2_date ').text()
                    item['REVIEWER']=sub_selector('[style="color:#979797;font-size: 12px;"]').eq(0).text()
                    item['REVIEWER_JOB']=sub_selector('.block_review_text_color3').eq(0).text()
                    item['REVIEW_TITLE']=sub_selector('.block_review_text_color2').eq(0).text()
                    item['REVIEW_TEXT']= sub_selector('.block_review_2_messages').text().replace('"','').replace("'",'').replace('\\','')
                    item['MEDLEM'] = ''
                    item['MEMBER_SINCE'] = ''
                    # yield item
                    yield JsonRequest('https://bitrixapi.haandvaerker.dk/v1/review/addHvdkReview' ,
                                      headers ={'Authorization':'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.'
                                                                'eyJpc3MiOiJodHRwczpcL1wvYml0cml4YXBpLmhhYW5kdmFlcmtlci'
                                                                '5ka1wvdjFcL2F1dGhcL2xvZ2luIiwiaWF0IjoxNjIyMjc4ODk0LCJle'
                                                                'HAiOjE2MzgwNDY4OTQsIm5iZiI6MTYyMjI3ODg5NCwianRpIjoiRllme'
                                                                'DhwS09ROU1aYXY2cyIsInN1YiI6MSwicHJ2IjoiODdlMGFmMWVmOWZkM'
                                                                'TU4MTJmZGVjOTcxNTNhMTRlMGIwNDc1NDZhYSJ9._DA_j1yUXQbr'
                                                                'EblywkeG6s_EnaNmqyvLv5OH7w5eH34'
                                                                ,}, data= item,callback=self.parse_reviews_data)
        except:
                selector = pq(response.body)
                for review in selector('.review'):
                    sub_selector = pq(review)
                    item['REVIEW_RATING']=sub_selector('.new_stars_block_20').attr('title').replace("/5","")
                    item['REVIEW_DATE']=sub_selector('.block_review_2_date ').text()
                    item['REVIEWER']=sub_selector('[style="color:#979797;font-size: 12px;"]').eq(0).text()
                    item['REVIEWER_JOB']=sub_selector('.block_review_text_color3').eq(0).text()
                    item['REVIEW_TITLE']=sub_selector('.block_review_text_color2').eq(0).text()
                    item['REVIEW_TEXT']= sub_selector('.block_review_2_messages').text().replace('"','').replace("'",'').replace('\\','')
                    item['MEDLEM'] = ''
                    item['MEMBER_SINCE'] = 'https://bitrixapi.haandvaerker.dk/v1/review/addHvdkReview'

                    # yield item
                    yield JsonRequest('', headers ={'Authorization':'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc'
                                                                    '3MiOiJodHRwczpcL1wvYml0cml4YXBpLmhhYW5kdmFlcmtlci5'
                                                                    'ka1wvdjFcL2F1dGhcL2xvZ2luIiwiaWF0IjoxNjIyMjc4ODk0L'
                                                                    'CJleHAiOjE2MzgwNDY4OTQsIm5iZiI6MTYyMjI3ODg5NCwian'
                                                                    'RpIjoiRllmeDhwS09ROU1aYXY2cyIsInN1YiI6MSwicHJ2IjoiO'
                                                                    'DdlMGFmMWVmOWZkMTU4MTJmZGVjOTcxNTNhMTRlMGIwNDc1NDZh'
                                                                    'YSJ9._DA_j1yUXQbrEblywkeG6s_EnaNmqyvLv5OH7w5eH34',},
                                                                    data= item,callback=self.parse_reviews_data)