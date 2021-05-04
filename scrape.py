import requests
from lxml import html
import json
from datetime import datetime, timezone

# Get fund value
pageContent=requests.get('https://www.presidentsoffice.gov.lk/index.php/covid-19-fund/')
tree = html.fromstring(pageContent.content)
fundVal = tree.xpath('string(/html/body/div[3]/div/div/article/div/div/div[2]/div/div[2]/div/div[1]/h1/text())')
print('Fund value was LKR ', fundVal)

with open('data.json', 'r+') as persistentFile:
	# Load historical data
	historicalData = json.load(persistentFile)
	if not 'history' in historicalData:
		historicalData['history'] = []

	# Build latest data
	data = {}
	data['value'] = fundVal
	data['time'] = datetime.utcnow().strftime('%B %d %Y - %H:%M:%S')
	historicalData['history'].append(data)

	# Save
	persistentFile.seek(0)
	json.dump(historicalData, persistentFile)
	persistentFile.truncate()