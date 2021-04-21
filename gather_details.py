# -*- coding: utf-8 -*-
import re
from tld import get_tld
import scrapy
from scrapy.crawler import CrawlerProcess
import sys
from scrapy import Selector
from scrapy.utils.project import get_project_settings
from scrapy.settings import Settings


class GatherDetailsSpider (scrapy.Spider):
    name = 'gather_details'
    greedy = True
    # domain = 'inspirant.ch'
    print ("Klasse ",sys.argv[1])

    # custom_settings = {'DOWNLOD_DELAY': 1}
    email_regex = re.compile (r"[-.a-z]+@[^@\s\.]+\.[.a-z]{2,3}")
    forbidden_keys = ['tel:' , 'mailto:' , '.jpg' , '.pdf' , '.png']
    allowed_domains = [f'{sys.argv[1]}']
    start_urls = [f'https://{sys.argv[1]}']

    # def __init__(self , domain):
    #     print ("init")
    #     self.allowed_domains = [f'{domain}']
    #     self.start_urls = [f'https://{domain}']
    #     super ().__init__

    def parse(self , response):
        try:
            html = response.body.decode ('utf-8')
        except UnicodeDecodeError:
            return
        emails = []
        phones = []
        print ("parse")
        # Find mailto's
        mailtos = response.xpath ("//a[starts-with(@href, 'mailto')]/@href").getall ()
        tels = response.xpath ("//a[starts-with(@href, 'tel:')]/@href").getall ()
        phones += [tel.replace ("tel:" , "") for tel in tels]
        emails = [mail.replace ('mailto:' , '') for mail in mailtos]
        body_emails = self.email_regex.findall (html)
        emails += [email for email in body_emails if \
                   get_tld ('https://' + email.split ('@')[-1] , fail_silently=True)]
        yield {
            'emails': list (set (emails)) ,
            'phones': list (set (phones)) ,
            'page': response.request.url
        }
        if self.greedy:
            links = response.xpath ("//a/@href").getall ()
            # If there are external links, scrapy will block them
            # because of the allowed_domains setting
            for link in links:
                skip = False
                for key in self.forbidden_keys:
                    if key in link:
                        skip = True
                        break
                if skip:
                    continue
                try:
                    yield scrapy.Request (link , callback=self.parse)
                except ValueError:
                    try:
                        yield response.follow (link , callback=self.parse)
                    except:
                        pass



# process = CrawlerProcess(settings={
#     "FEEDS": {
#         "out1.json": {"format": "json"},
#     },
# })
# process.crawl(GatherDetailsSpider)
# process.start()

# def startparse(domains):
print ("initparse")
 # Modul sys wird importiert:
#import sys

# Iteration über sämtliche Argumente:
# for eachArg in sys.argv:
#         print (eachArg)
process = CrawlerProcess (settings={
    "FEEDS": {
        "emails.json": {"format": "json"} ,
    } ,
    'USER_AGENT': 'Mozilla/5.0' ,
})
print ("start Gather_detail")
process.crawl (GatherDetailsSpider)
# GatherDetailsSpider.domain = sys.argv[1]
process.start ()
