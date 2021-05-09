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

def getLastDonatedAt():
	arr = donationsTree.xpath('string(//*[@id="donated-list"]/tbody/tr[1]/td[1]/text())').split(' ')
	return ' '.join([arr[-3], arr[-2], arr[-1]])

def getLastDonatedBy():
	return donationsTree.xpath('string(//*[@id="donated-list"]/tbody/tr[1]/td[1]/text())').split()[0]

def getDonationCount():
	return donationsTree.xpath('string(/html/body/div[1]/div[2]/section[2]/div/div/div[2]/div[4]/div/h3/span/text())')

def getLastDonatedAmount():
	return donationsTree.xpath('string(//*[@id="donated-list"]/tbody/tr[1]/td[2]/text())')

def getFundValue():
	return fundTree.xpath('string(/html/body/div[1]/div[2]/section[1]/div/div[2]/div[1]/div/div[1]/span/i/text())')

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
donationData['lastDonatedAt'] = getLastDonatedAt()
donationData['lastDonatedBy'] = getLastDonatedBy()
donationData['lastUpdated'] = time
print('Donatins: ', donationData)

with open('data.json', 'r+') as persistentFile:
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