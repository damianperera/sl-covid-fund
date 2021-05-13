import requests
from lxml import html
import json
from datetime import datetime

# Execution time
time = datetime.now().isoformat()

fundSource = 'https://www.itukama.lk/'
fundContent = requests.get(fundSource)
fundTree = html.fromstring(fundContent.content)

donationsSource = 'https://www.itukama.lk/donate-now/'
donationsContent = requests.get(donationsSource)
donationsTree = html.fromstring(donationsContent.content)

# enhancement: scrape both webpages asynchronously

def getFundValue():
	return fundTree.xpath('string(//*[contains(@class, "donate-fill")]/span/i/text())')

def getLastDonatedAt():
	arr = donationsTree.xpath('string(//*[@id="donated-list"]/tbody/tr[1]/td[1]/text())').split(' ')
	return ' '.join([arr[-3], arr[-2], arr[-1]])

def getLastDonatedBy():
	return donationsTree.xpath('string(//*[@id="donated-list"]/tbody/tr[1]/td[1]/text())').split()[0]

def getDonationCount():
	return donationsTree.xpath('string(//*[@class="donator-count"]/span/text())')

def getLastDonatedAmount():
	return donationsTree.xpath('string(//*[@id="donated-list"]/tbody/tr[1]/td[2]/text())')

def getDonations():
        return list(map(int, [val.replace(',','') for val in donationsTree.xpath('//*[@id="donated-list"]/tbody//td[2]/text()')]))

# Build latest fund data
fundData = {}
fundData['value'] = getFundValue()
fundData['source'] = fundSource
fundData['time'] = time
print('Fund: ', fundData)

# Build latest donation data
donationData = {}
donationData['count'] = getDonationCount()
donationData['lastDonatedAmount'] = getLastDonatedAmount()
donationData['lastDonatedAt'] = getLastDonatedAt() # enhancement: change to ISO 8601 format
donationData['lastDonatedBy'] = getLastDonatedBy()
donationData['totalPublicDonationAmount'] = f'{(sum(getDonations())):,}' # formats int to currency string
donationData['lastUpdated'] = time
donationData['source'] = donationsSource
print('Donations: ', donationData)

with open('data.json', 'r+') as persistentFile: # enhancement: add support for CSV
	# Load historical data
	historicalData = json.load(persistentFile)
	historicalData['lastUpdated'] = time

	if not 'donations' in historicalData or historicalData['donations']['count'] != donationData['count']:
		historicalData['donations'] = donationData

	if not 'history' in historicalData:
		historicalData['history'] = []
		historicalData['history'].append(fundData)
	elif historicalData['history'][-1]['value'] != fundData['value']:
		historicalData['history'].append(fundData)

	# Save
	persistentFile.seek(0)
	json.dump(historicalData, persistentFile)
	persistentFile.truncate()
