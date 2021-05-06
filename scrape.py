import requests
from lxml import html
import json
from datetime import datetime, timezone

# Execution time
time = datetime.now().isoformat()

# Get fund value
pageContent=requests.get('https://www.itukama.lk/')
tree = html.fromstring(pageContent.content)
fundVal = tree.xpath('string(/html/body/div[1]/div[2]/section[1]/div/div[2]/div[1]/div/div[1]/span/i/text())')
print('Fund value was LKR ', fundVal)

with open('data.json', 'r+') as persistentFile:
	# Load historical data
	historicalData = json.load(persistentFile)
	historicalData['lastUpdated'] = time

	data = {}
	data['value'] = fundVal
	data['time'] = time

	if not 'history' in historicalData:
		historicalData['history'] = []
		historicalData['history'].append(data)
	elif historicalData['history'][-1]['value'] != fundVal:
		# Build latest data
		historicalData['history'].append(data)

	# Save
	persistentFile.seek(0)
	json.dump(historicalData, persistentFile)
	persistentFile.truncate()
