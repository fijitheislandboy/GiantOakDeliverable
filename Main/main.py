import scrapy,copy,requests,json
from lxml import html
#utilizing the scrapy library v2.5.0
#I chose to utilize this source because there were no restrictions given on libraries
#that could be used for this deliverable.
#Link to documentation: https://docs.scrapy.org/en/latest/
#This script probably would not multithread well in its current state, considering that I use global variables and have
#two scrapers that use the same Array
wantedPerson = {'First Name': '',
                'Last Name': '',
                'Information': {
                    'Offense':'','Crime Location': '', 'Crime Date': ' ', 'Ethnic Appearance': '', 'Height':'','Build':'','Gender': '', 'Hair Color':'','Hair Length':''},
                'Other': {'Crime Details': '', 'Notable Features': ''}
                }
sublinks = []
completeLinks = []
personArray = []
toJson = {"source_code":"UK_MWL","source_name":"UK Most Wanted List","source_url":"https://www.nationalcrimeagency.gov.uk/most-wanted-search","persons": personArray}
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
        siteUrl = "https://www.nationalcrimeagency.gov.uk"
        sublinks.append(appendUrl)
        return siteUrl + appendUrl
# A function that takes in three arguments, the index of the location of the dict in personArray containing the criminal's
    #information, the crime information, and the biographical information

    #Function to use the Crawler and parse the information from the website. Must be given the name parse in order
    #for the module to utilize it
    def parse(self, response, **kwargs):
        global retrievedData, personArray, wantedPerson, sublinks, completeLinks
        siteData = response.xpath("//a[contains(@href, '/most-wanted/')]").extract()
        retrievedData = siteData
        for i in range(0,len(retrievedData)):
            wantedPerson['First Name'],wantedPerson['Last Name'] = crawler.nameExtractor(self,retrievedData[i])
            completeLinks.append(crawler.sublinkExtractor(self,retrievedData[i]))
            personArray.append(copy.deepcopy(wantedPerson))
        crawler.subLinkSearcher(self)
        with open('CrawlerOutput.json','w') as output:
            json.dump(toJson,output)
        print('done')
    def subLinkSearcher(self):
        # using a selector to retrieve the relevant page content
        global retrievedData, personArray, wantedPerson, sublinks, completeLinks
        checkList = ['Location: ', 'Date of Incident: ', 'Crime: ', 'Sex: ', 'Height: ', 'Build: ', 'Hair Colour: ', 'Hair Length: ',
                     'Ethnic Appearance: ', 'Additional Information: ']
        for url in completeLinks:
            biographicalData = []
            mydata = requests.get(url)
            xmltree = html.fromstring(mydata.content)
            data = xmltree.xpath("//*[@class='item-page most-wanted-grid']")
            try:
                accusedOf = xmltree.xpath('//*[@id="content"]/div/div[3]/div[3]/p/text()')[0]
            except:
                accusedOf = xmltree.xpath('// *[ @ id = "content"] / div / div[3] / div[3] / p / span/text()')[0]

            biographicalData = xmltree.xpath("//*[@class='item-page most-wanted-grid']//span/text()")
            for title in range(0,len(biographicalData)):
                biographicalData[title] = str(biographicalData[title])
            # if (len(biographicalData) < 20):
            #     biographicalDataCopy = [20]
            #     for j in range(len(biographicalData), 20):
            #         biographicalData.append('Not Given')
            for category in checkList:
                try:
                    biographicalData.index(category)
                except ValueError:
                        biographicalData.append(category)
                        biographicalData.append('Not Given')
            updatePerson = completeLinks.index(url)
            personalInformation = ()
            entry = personArray[updatePerson]
            entry['Information']['Offense'] = biographicalData[biographicalData.index('Crime: ') + 1]
            entry['Information']['Crime Location'] =biographicalData[biographicalData.index('Location: ') + 1]
            entry['Information']['Crime Date'] = biographicalData[biographicalData.index('Date of Incident: ') + 1]
            entry['Information']['Ethnic Appearance'] = biographicalData[ biographicalData.index('Ethnic Appearance: ') + 1]
            entry['Information']['Height'] = biographicalData[biographicalData.index('Height: ') + 1]
            entry['Information']['Build'] = biographicalData[biographicalData.index('Build: ') + 1]
            entry['Information']['Gender'] = biographicalData[biographicalData.index('Sex: ') + 1]
            entry['Information']['Hair Color'] = biographicalData[biographicalData.index('Hair Colour: ') + 1]
            entry['Information']['Hair Length'] = biographicalData[biographicalData.index('Hair Length: ') + 1]
            entry['Other']['Crime Details'] = accusedOf
            entry['Other']['Notable Features'] = biographicalData[biographicalData.index('Additional Information: ') + 1]

            personalInformation = ()
            personArray[updatePerson] = entry
            # item = {'Replyinfo': xmltree.xpath("//*[@class='item-page most-wanted-grid']//span/text()").extract()}
        return personArray
