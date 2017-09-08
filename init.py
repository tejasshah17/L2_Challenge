from flask import Flask, render_template, request
from fetchData import init
from analyzeData import getData

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
	try:
		if request.method == 'GET':
			return render_template('index.html')
		else:
			start_date = request.form['startDate']
			end_date = request.form['endDate']
			search_type = request.form['search_type']

			data_top3, data_manufacturer, data_correlation, data_volatility = getData(search_type, start_date, end_date)
			return render_template('index.html', start_date=start_date, end_date=end_date,
								   brand_percent=data_manufacturer, top3=data_top3, volatility = data_volatility,
								   correlation=data_correlation, search_type=search_type)

	except Exception as ex:
		return render_template('404.html',error_code=repr(ex))


if __name__ == '__main__':
	try:
		init()
		app.run()

	except Exception as ex:
		print ex
