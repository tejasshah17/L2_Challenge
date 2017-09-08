import requests
import json
import os
import folder_loc as fl
import datetime as dt
import pandas as pd
import time


class fetchData:
	BBKEY =  'YOURKEY'
	api_endpoint = "https://api.bestbuy.com/v1/products"

	stv_search = """((search=Smart&search=TV*)&(categoryPath.id=abcat0101000)|
		(categoryPath.id=abcat0101000&manufacturer=Toshiba&smartCapable=true))"""

	cstv_search = """((search=Curved&search=Smart&search=TV)&(categoryPath.id=abcat0101000)
		&name=Curved%20Smart%20TV*)"""

	stv_url = api_endpoint+stv_search
	cstv_url = api_endpoint+cstv_search


def init():
	try:
		############### -- CREATE DATA FOLDERS -- ###############
		ret_code, ret_status = fl.createFolder()
		print ret_status

		############### -- REQUEST CURVED SMART TV DATA -- ############
		requestData('CSTV')
		requestData('STV')


	except Exception as ex:
		return repr(ex)

def makeRequest(resultdf,search_type,pageNum=1):
	try:
		if search_type == "CSTV":
			url = fetchData.cstv_url
		else:
			url = fetchData.stv_url

		currentPage = 0
		totalPages = -1

		while currentPage != totalPages:
			resp = requests.get(url, {'apiKey': fetchData.BBKEY, 'sort': 'salesRankShortTerm.asc,bestSellingRank.asc',
									  'facet': 'manufacturer',
									  'pageSize': 50, 'page': pageNum, 'format': 'json',
									  'show': 'sku,manufacturer,name,salesRankShortTerm,salesRankMediumTerm,salesRankLongTerm,bestSellingRank,customerReviewAverage,customerReviewCount,image,url'})

			json_data = json.loads(resp.content)

			json_file_name = "{}_JSON_{}_P{}.json".format(search_type,
														  dt.datetime.strftime(dt.datetime.now(), '%Y_%m_%d'), pageNum)
			json_file_path = os.path.join(fl.json_data_path, json_file_name)

			f = open(json_file_path, 'w+')
			f.write(resp.content)
			f.close()
			print "{} JSON Page-{} File Created Successfully !!".format(search_type,pageNum)

			products = json_data['products']
			df = pd.DataFrame(products,
							  columns=['date', 'sku', 'manufacturer', 'name', 'salesRankShortTerm', 'salesRankMediumTerm',
									   'salesRankLongTerm',
									   'bestSellingRank', 'customerReviewAverage', 'customerReviewCount', 'image', 'url'])

			resultdf = resultdf.append(df,ignore_index=True)
			currentPage = json_data['currentPage']
			totalPages = json_data['totalPages']
			pageNum = currentPage + 1
			time.sleep(1)
		return resultdf

	except Exception as ex:
		print ex

def requestData(search_type):
	try:
		json_file_name = "{}_JSON_{}_P{}.json".format(search_type,
													  dt.datetime.strftime(dt.datetime.now(), '%Y_%m_%d'), 1)
		json_file_path = os.path.join(fl.json_data_path, json_file_name)

		csv_file_name = "{}_CSV_{}.csv".format(search_type, dt.datetime.strftime(dt.datetime.now(), '%Y_%m_%d'))
		csv_file_path = os.path.join(fl.csv_data_path, csv_file_name)

		if os.path.exists(json_file_path) and os.path.exists(csv_file_path):
			return "{} Data already received for today".format(search_type)


		resultdf = pd.DataFrame()
		resultdf = makeRequest(resultdf,search_type)

		resultdf['date'] = dt.datetime.strftime(dt.datetime.now(), '%Y_%m_%d')

		if not os.path.exists(csv_file_path):
			resultdf.to_csv(csv_file_path, index=False, encoding='utf-8')
		else:
			with open(csv_file_path, 'a') as f:
				resultdf.to_csv(f, header=False, index=False, encoding='utf-8')
		return "{} CSV File Created Successfully !!".format(search_type)

	except Exception as ex:
		return repr(ex)

if __name__ == "__main__":
	init()