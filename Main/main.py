import scrapy
#import Driver.Crawler
#utilizing the scrapy library v2.5.0
#I chose to utilize this source because there were no restrictions given on libraries
#that could be used for this deliverable.
#Link to documentation: https://docs.scrapy.org/en/latest/

class crawler(scrapy.Spider):
    start_urls = ['https://www.nationalcrimeagency.gov.uk/most-wanted-search']
    name = "UKMostWanted"
    def parse(self, response, **kwargs):
        print(response.xpath("//a[contains(@href, '/most-wanted/')]").extract())
        print("hi")
