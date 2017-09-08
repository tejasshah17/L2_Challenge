import folder_loc as fl
import pandas as pd
import os


def getData(search_type, start_date, end_date):
	try:
		dateList = list(pd.date_range(start_date, end_date, freq='D'))
		df_result = pd.DataFrame()
		df_top3 = pd.DataFrame()
		for date in dateList:
			fileName = "{}_CSV_{}.csv".format(search_type, pd.datetime.strftime(date, '%Y_%m_%d'))
			filePath = os.path.join(fl.csv_data_path, fileName)
			if os.path.exists(filePath):
				fileContent = pd.read_csv(filePath)
				df_top3 = df_top3.append(fileContent.head(3))
				df_result = df_result.append(fileContent)

		if not df_top3.empty:
			result_top3 = getBrandPercent(df_top3, "top3")
		else:
			result_top3 = None
		if not df_result.empty:
			result_manufacturer = getBrandPercent(df_result)
			result_correlation = getReviewCorrelation(df_result)
			result_volatility = getVolatility(df_result)
		else:
			result_manufacturer = result_correlation = result_volatility = None
		return result_top3, result_manufacturer, result_correlation, result_volatility


	except Exception as ex:
		return repr(ex)


def getReviewCorrelation(df):
	corr_shortRank_reviewCount = "{0:.3f}".format(df['salesRankShortTerm'].corr(df['customerReviewCount']))
	corr_medRank_reviewCount = "{0:.3f}".format(df['salesRankMediumTerm'].corr(df['customerReviewCount']))
	corr_longRank_reviewCount = "{0:.3f}".format(df['salesRankLongTerm'].corr(df['customerReviewCount']))
	corr_bestRank_reviewCount = "{0:.3f}".format(df['bestSellingRank'].corr(df['customerReviewCount']))

	corr_shortRank_reviewAvg = "{0:.3f}".format(df['salesRankShortTerm'].corr(df['customerReviewAverage']))
	corr_medRank_reviewAvg = "{0:.3f}".format(df['salesRankMediumTerm'].corr(df['customerReviewAverage']))
	corr_longRank_reviewAvg = "{0:.3f}".format(df['salesRankLongTerm'].corr(df['customerReviewCount']))
	corr_bestRank_reviewAvg = "{0:.3f}".format(df['bestSellingRank'].corr(df['customerReviewAverage']))

	correlations = {'reviewCount': [corr_shortRank_reviewCount, corr_medRank_reviewCount, corr_longRank_reviewCount, corr_bestRank_reviewCount],
					'reviewAvg': [corr_shortRank_reviewAvg, corr_medRank_reviewAvg, corr_longRank_reviewAvg, corr_bestRank_reviewAvg]}
	return correlations


def getVolatility(df):
	df_volatile = df.groupby(['sku', 'manufacturer']).std().reset_index()
	df_volatile.sort_values(by=['manufacturer'], inplace=True)

	df_vol_manufacturer = df_volatile.groupby(['manufacturer']).mean().round(2).reset_index()
	df_vol_manufacturer = df_vol_manufacturer.set_index('manufacturer').transpose()
	all_brands = ['LG','Samsung','Sony','Toshiba']
	columns = df_vol_manufacturer.columns
	missing_cols = [item for item in all_brands if item not in columns]
	for col in missing_cols:
		df_vol_manufacturer[col] = "--"
	df_vol_manufacturer = df_vol_manufacturer[all_brands]

	return df_vol_manufacturer.to_dict(orient='list')


def getBrandPercent(df,category=None):
	df_manufacturer = pd.DataFrame({'count':df.groupby(['manufacturer']).size()}).reset_index()
	total_cnt = df_manufacturer['count'].sum()
	df_manufacturer['percent'] = (df_manufacturer['count']/total_cnt)*100
	df_manufacturer['percent'] = df_manufacturer['percent'].round(2)
	df_manufacturer.sort_values(by=['percent'],ascending=False,inplace=True)

	if category == "top3":
		all_brands = ['LG', 'Samsung', 'Sony', 'Toshiba']
		set_brands = set(df_manufacturer['manufacturer'].tolist())

		missing_brand = [item for item in all_brands if item not in set_brands]
		for brand in missing_brand:
			df_manufacturer = df_manufacturer.append({'manufacturer':brand,'count':0,'percent':0.00},ignore_index=True)
	return df_manufacturer.to_dict(orient='list')
