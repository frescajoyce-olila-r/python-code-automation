import scrapy
from selenium import webdriver
from scrapy import Selector
from selenium.webdriver.chrome.options import Options
from scrapy.http import Request
from time import sleep
import pandas as pd
import os

TIMEOUT = 60

class InstallerSpider(scrapy.Spider):
    name = 'installer'
    allowed_domains = ['installator.dk']
    start_urls = ['https://installator.dk/partnere/']
    start_index = 1
    item_start_index = 1

    def parse(self, response):
        yield Request(response.url, callback=self.process_item)

    def process_item(self, response):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--log-level=3")
        chrome_options.add_argument('--ignore-certificate-errors')
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-infobars")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--enable-precise-memory-info")
        chrome_options.add_argument('lang=en')
        chrome_options.add_experimental_option('prefs', {'intl.accept_languages': 'en,en_US'})
        driver = webdriver.Chrome(options=chrome_options)

        driver.get(response.url)
        sleep(10)
        driver.find_element_by_class_name("chosen-single").click()
        contents = []

        while len(driver.find_elements_by_xpath(f'//li[@data-option-array-index="{self.start_index}"]')) > 0:
            option = driver.find_element_by_xpath(f'//li[@data-option-array-index="{self.start_index}"]')
            print(f"Option: {option.text}")
            option_text = option.text
            option.click()
            driver.find_element_by_id('edit-submit').click()

            current_url = driver.current_url
            while len(driver.find_elements_by_class_name(f'item-list__item:nth-child({self.item_start_index})')) > 0:
                item = driver.find_element_by_class_name(f'item-list__item:nth-child({self.item_start_index})')
                item.click()
                sleep(10)
                sel = Selector(text=driver.page_source)

                company_name = sel.css('.h2.drupaledit::text')
                if company_name:
                    company_name = company_name.extract_first().strip()
                else:
                    company_name = 'N/A'

                website = sel.css('.meta-section__title>a::text')
                if website:
                    website = website.extract_first().strip()
                else:
                    website = 'N/A'

                telephone = sel.css('.list.list--fa>li:nth-child(2)::text')
                if telephone:
                    telephone = telephone.extract_first().strip()
                else:
                    telephone = 'N/A'

                address = sel.css('.list.list--fa>li:nth-child(3)::text')
                if address:
                    address = address.extract_first().strip()
                else:
                    address = 'N/A'

                email = sel.css('.list.list--fa>li:first-child>a::text')

                if email:
                    email = email.extract_first().strip()
                else:
                    email = 'N/A'

                contact_person =sel.css('.item-list__item.grid-2-6 .item-list__content .item-list__headline::text')
                if contact_person:
                    contact_person = contact_person.extract_first().strip()
                else:
                    contact_person ='N/A'

                contact_number = sel.css('.item-list__content .list.list--fa >li:nth-child(2)::text')
                if contact_number:
                    contact_number = contact_number.extract_first().strip()
                else:
                    contact_number ='N/A'

                contact_email = sel.css('.item-list__content .list.list--fa a::attr(href)')
                if contact_email:
                    contact_email =contact_email.extract_first().strip()
                else:
                    contact_email ='N/A'

                contents.append([option_text, company_name, website, telephone, address, email,contact_person,contact_number,contact_email])

                yield {
                    'Option': option_text,
                    'Company Name': company_name,
                    'Website': website,
                    'Phone Number': telephone,
                    'Address': address,
                    'Company Email': email,
                    'Contact Person ': contact_person,
                    'Contact Person Phone Number': contact_number,
                    'Contact Person Email': contact_email,
                }

                self.item_start_index += 1
                driver.get(current_url)
                sleep(10)
            self.item_start_index = 1
            self.start_index += 1
            driver.get(response.url)
            sleep(10)
            driver.find_element_by_class_name("chosen-single").click()


        dirname = os.path.dirname(__file__)
        filename = os.path.join(dirname, '../../../installator.xlsx')

        df = pd.DataFrame(contents, columns=[
            'Option',
            'Company Name',
            'Website',
            'Phone Number',
            'Address',
            'Company Email',
            'Contact Person',
            'Contact Person Phone Number',
            'Contact Person Email'

        ])
        df.to_excel(filename, index=False)

        driver.quit()


