import scrapy,copy
from scrapy import Request
#import Driver.Crawler
#utilizing the scrapy library v2.5.0
#I chose to utilize this source because there were no restrictions given on libraries
#that could be used for this deliverable.
#Link to documentation: https://docs.scrapy.org/en/latest/
global retrievedData,personArray,wantedPerson,sublinks
#This script probably would not multithread well in its current state, considering that I use global variables and have
#two scrapers that use the same Array
wantedPerson = {'First Name': '',
                'Last Name': '',
                'Information': {
                    'DOB': 'Not Given By This Site', 'Place of Birth': 'Not Given By This Site', 'Nationality': '', 'Gender': '', },
                'Other': {'Crime': '', 'Notable Features': ''}
                }
sublinks = []
personArray = []
class crawler(scrapy.Spider):
    #start_urls and name are variable names required by the module in order for it to execute properly
    start_urls = ['https://www.nationalcrimeagency.gov.uk/most-wanted-search']
    name = "UKMostWanted"
    retrievedData = []

    # A function that takes in one argument, the html code for a wanted individual, and extracts their
    #first and last name.
    def nameExtractor(self,workString):
        workString = str(workString)
        startIndex = workString.find('<h3>') + 4
        endIndex = workString.find('</h3>')
        spaceIndex = workString.find(" ")
        nameIs = workString[startIndex:endIndex]
        firstName = nameIs[0:nameIs.find(" ")]
        lastName = nameIs[nameIs.find(" "):len(nameIs)]
        return firstName,lastName
# A function that takes in one argument, the html code for a wanted individual, and extracts the href for their
    # biographical information
    def sublinkExtractor(self,workString):
        workString = str(workString)
        startIndex = workString.find('/most-wanted')
        tag = workString[startIndex:len(workString)]
        appendUrl = tag[:tag.find('>') - 1]
        siteUrl = "https://www.nationalcrimeagency.gov.uk/"
        return siteUrl + appendUrl
# A function that takes in three arguments, the index of the location of the dict in personArray containing the criminal's
    #information, the crime information, and the biographical information
    def wantedPersonUpdater(self,indexNum,crimeInfo,personalInfo):

        return
    #Function to use the Crawler and parse the information from the website. Must be given the name parse in order
    #for the module to utilize it
    def parse(self, response, **kwargs):
        siteData = response.xpath("//a[contains(@href, '/most-wanted/')]").extract()
        retrievedData = siteData
        for i in range(0,len(retrievedData)):
            wantedPerson['First Name'],wantedPerson['Last Name'] = crawler.nameExtractor(self,retrievedData[i])
            sublinks.append(crawler.sublinkExtractor(self,retrievedData[i]))
            personArray.append(copy.deepcopy(wantedPerson))
        for j in range(0,len(sublinks)):
            goTo = sublinks[j]
            yield Request(url=goTo,callback=self.subLinkSearcher)
    def subLinkSearcher(self,response):
        #using a selector to retrieve the relevant page content
         data = response.xpath("//*[@class='item-page most-wanted-grid']").extract()
         accusedOf = response.xpath("//div[@itemprop='articleBody']").extract()
         biographicalData = response.xpath("//*[@class='item-page most-wanted-grid']//span/text()").extract()
         crimeInfoStart = str(accusedOf).find("<p>")
         crimeInfoend = str(accusedOf).find("</p>")
         accussedOf = str(accusedOf)
         crimeInfo = accussedOf[crimeInfoStart+3:crimeInfoend]
         updatePerson = sublinks.index(response.url)
         crawler.wantedPersonUpdater(self,updatePerson,crimeInfo,)
         print(data)


