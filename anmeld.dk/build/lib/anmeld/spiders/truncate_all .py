from scrapy import Spider , Request,FormRequest
from pyquery import PyQuery as pq
import json
import re
import requests


class AnmeldSpiderSpider(Spider):
	name = 'truncate_all'

	def __init__(self, *args, **kwargs):
		self.start_urls = ['https://bitrixapi.haandvaerker.dk/v1/review/truncateHvdkReview']
	def start_requests(self):
		headers = {'Authorization':'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczpcL1wvYml0cml4YXBpLmhhYW5kdmFlcmtlci5ka1wvdjFcL2F1dGhcL2xvZ2luIiwiaWF0IjoxNjIyMjc4ODk0LCJleHAiOjE2MzgwNDY4OTQsIm5iZiI6MTYyMjI3ODg5NCwianRpIjoiRllmeDhwS09ROU1aYXY2cyIsInN1YiI6MSwicHJ2IjoiODdlMGFmMWVmOWZkMTU4MTJmZGVjOTcxNTNhMTRlMGIwNDc1NDZhYSJ9._DA_j1yUXQbrEblywkeG6s_EnaNmqyvLv5OH7w5eH34',}
		for page in self.start_urls:
			yield Request(page, method='GET',headers=headers, callback=self.parse )

	def parse(self , response):
		yield json.loads(response.text)
