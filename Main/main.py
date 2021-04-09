import scrapy

#utilizing the scrapy library v2.5.0
#Link to documentation: https://docs.scrapy.org/en/latest/
class Driver(scrapy.Spider):
    toScrape = ['https://www.nationalcrimeagency.gov.uk/most-wanted-search']
    scraperName = ""