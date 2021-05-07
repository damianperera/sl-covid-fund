import requests
from lxml import html
import json
import csv
from datetime import datetime

source = 'https://www.itukama.lk/'

# Execution time
time = datetime.now().isoformat()

# Get fund value
pageContent = requests.get(source)
tree = html.fromstring(pageContent.content)
fundVal = tree.xpath('string(/html/body/div[1]/div[2]/section[1]/div/div[2]/div[1]/div/div[1]/span/i/text())')
fundVal = float(fundVal.replace(',', ''))
print('Fund value was LKR ', fundVal)

# Build latest data
data = {}
data['time'] = time
data['value'] = fundVal
data['source'] = source

with open('data.json', 'r+') as persistentFile:
	# Load historical data
	historicalData = json.load(persistentFile)
	historicalData['lastUpdated'] = time

	if not 'history' in historicalData:
		historicalData['history'] = []
		historicalData['history'].append(data)
	elif historicalData['history'][-1]['value'] != fundVal:
		historicalData['history'].append(data)

	# Save
	persistentFile.seek(0)
	json.dump(historicalData, persistentFile)
	persistentFile.truncate()

with open("data.csv", mode='a+', newline='') as csvFile:
	writer = csv.DictWriter(csvFile, data.keys())
	writer.writerow(data)