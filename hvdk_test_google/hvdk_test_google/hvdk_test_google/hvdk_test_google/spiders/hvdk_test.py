from scrapy import Spider, Request
from pyquery import PyQuery as pq
import pandas as pd
import os
import re
from time import sleep
from urllib.parse import quote_plus

URL = 'https://master.haandvaerker.dk'


class HvdkTestSpider(Spider):
    name = 'hvdk_test'
    http_user = 'test'
    http_pass = 'Ole12345'

    def parse(self, response):
        print(len(pq(response.body)('table > tr')))
        for idx, link in enumerate([pq(x)('a').eq(0) for x in pq(response.body)('table > tr > td:nth-child(3)')]):
            if idx == 0:
                continue
            pattern = r'(?P<name>.*?) - (?P<port>\d+)'
            search = re.search(pattern, link.text())
            groupdict = search.groupdict()
            name = groupdict['name']
            port = groupdict['port']
            url_parts = link.attr('href').rsplit('/', 1)
            base_url = url_parts[0]
            last_uri = url_parts[-1]
            url = f'{base_url}/{quote_plus(last_uri)}'

            print(f'URL: {url}')

            sleep(10)
            yield Request(url, callback=self.parse_results, cb_kwargs=dict(name=name, url=url, port=port))
            print(f'Success')

    def parse_results(self, response, name, url, port):
        print(f"RESULT")
        selector = pq(response.body)
        name_value = selector('#search > div > div > div:first-child h3').text()
        port_text = selector('#search > div > div > div:first-child span[role="text"]:first-child').text()
        port_pattern = r' › (\d+)'
        port_search = re.search(port_pattern, port_text)
        port_value = port_search.group(1)
        contents = []

        if name_value == name and port_value == port:
            print(f"Result found")
            contents.append([name, port, url, 'Yes'])
        else:
            print(f"Result not found")
            contents.append([name, port, url, 'No'])

        yield {
            'Name': name,
            'Port': port,
            'URL': url
        }

        dirname = os.path.dirname(__file__)
        filename = os.path.join(dirname, '../../../google_search.xlsx')

        df = pd.DataFrame(contents, columns=[
            'Name',
            'Port'
            'URL',
            'Is showing on google?'
        ])
        df.to_excel(filename, index=False)
