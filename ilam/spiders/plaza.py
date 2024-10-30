from scrapy.spiders import CrawlSpider ,Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from bs4 import BeautifulSoup
import requests
from ilam.items import IlamItem
import json


class PlazaCrawler(CrawlSpider):
    name = 'plaza'
    allowed_domain = 'www.gooshiplaza.com'
    start_urls = ['https://gooshiplaza.com/']

    rules = [
        Rule(LinkExtractor(allow=r'/product/'), callback='get_all_products' ,follow=True)
    ]

    def get_all_products(self ,response):
        l = ItemLoader(item=IlamItem(), selector=response)
        l.add_xpath('title' ,'//*[contains(concat( " ", @class, " " ), concat( " ", "wd-entities-title", " " ))]')
        l.add_xpath('price' ,'//*[contains(concat( " ", @class, " " ), concat( " ", "elementor-widget-wd_single_product_price", " " ))]//bdi/text()')
        l.add_value('page_url', response.url)
        register_available = ''
        warranty_f = response.xpath("//select[@id='pa_guarantee']/option/text()").extract()
        if warranty_f:
            filtered_options = [option for option in warranty_f if option != "یک گزینه را انتخاب کنید"]
            l.add_value('warranty', filtered_options)
        for r in warranty_f:
            if 'رجیستر' in r:
                register_available = 'رجیسترشده'
            else:
                register_available = 'رجیسترنشده'

        l.add_xpath('available', '//*[contains(concat( " ", @class, " " ), concat( " ", "wd-show", " " ))]/text()')

        gallery_list = response.xpath('//div[contains(@class, "wd-carousel-item")]//img/@data-large_image').getall()
        filter_url = list(set([url for url in gallery_list if url.startswith('https://gooshiplaza.com/')]))
        l.add_value('gallery_url',filter_url)
        image_urls = response.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "wp-post-image", " " ))]/@src').getall()
        if register_available:
            l.add_value('register', register_available)
        else:
            l.add_value('register', 'نامشخص')

        filtered_urls = [url for url in image_urls if url.startswith('https://gooshiplaza.com/')]
        l.add_value('img_url', filtered_urls)

        attributes = {}
        for row in response.css('tr.woocommerce-product-attributes-item'):
            key = row.css('th .wd-attr-name::text').get()
            value = row.css('.woocommerce-product-attributes-item__value p::text').get()
            if key:
                key = key.replace('\n', '').replace('\t', '').strip()
            if value:
                value = value.replace('\n', '').replace('\t', '').strip()
            else:
                value = 'نامشخص'
            attributes[key] = value
        attributes_json = json.dumps(attributes, ensure_ascii=False)
        l.add_value('org_price', attributes_json)

        caps = response.css('#tozihat > .elementor-widget-container h2::text, #tozihat > .elementor-widget-container p::text').getall()
        cap = ' '.join([c.replace('\n', '').replace('\t', '').strip() for c in caps if c.strip()])
        if not cap:
            cap = 'نامشخص'


        l.add_value('caption', cap)
        return l.load_item()
