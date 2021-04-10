import scrapy

class crawler(scrapy.Spider):
    toScrape = ['https://www.nationalcrimeagency.gov.uk/most-wanted-search']
    scraperName = "UKMostWanted"
    def parse(self, response, **kwargs):
        response.xpath('//a[contains(@href, "most-wanted"/@href').getall()
        print("hi")