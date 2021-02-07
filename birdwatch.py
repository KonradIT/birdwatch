import requests
import logging
from pprint import pprint as pp
import json
import glob
import os
from urllib.parse import urlparse
from typing import List
import csv_to_sqlite

class Secrets:
	def __init__(self, cookies: dict, headers: dict):
		self.cookies = cookies
		self.headers = headers
		
class Birdwatch:
	def __init__(self, auth: Secrets, debug: bool):
		self.auth=auth
		self.debug = debug
		logging.basicConfig(level=logging.DEBUG if debug else logging.ERROR)

	def fetch_public_data(self) -> dict:
		params = (
			('variables', '{}'),
		)

		response = requests.get('https://twitter.com/i/api/graphql/Y-NuXJ8gNFtPuS8GwXv21Q/BirdwatchFetchPublicData', headers=self.auth.headers, params=params, cookies=self.auth.cookies)
		assert(response.status_code == 200)
		return response.json()

	def save(self, data: dict, output="output"):
		captures = glob.glob(output + "/*")
		try:
			latest = max(captures, key=os.path.getmtime)
		except:
			latest = "0"
		createdat = data["data"]["birdwatch_latest_public_data_file_bundle"]["notes"]["created_at"]
		if int(createdat) > int(latest.replace(output+"/", "")):
			os.mkdir("{}/{}".format(output, createdat))
			filenames=[]
			for url in data["data"]["birdwatch_latest_public_data_file_bundle"]["notes"]["urls"]:
				a = urlparse(url)
				r = requests.get(url, allow_redirects=True)
				filename = "{}/{}/{}".format(output, createdat, os.path.basename(a.path))
				filenames.append(filename)
				open(filename, "wb").write(r.content)
	
			for url in data["data"]["birdwatch_latest_public_data_file_bundle"]["ratings"]["urls"]:
				a = urlparse(url)
				r = requests.get(url, allow_redirects=True)
				filename = "{}/{}/{}".format(output, createdat, os.path.basename(a.path))
				filenames.append(filename)
				open(filename, "wb").write(r.content)
    
			options = csv_to_sqlite.CsvOptions(delimiter="\t", typing_style="utf8", encoding="windows-1250") 
			csv_to_sqlite.write_csv(filenames, "{}/{}/{}".format(output, createdat, "database.sqlite"), options)