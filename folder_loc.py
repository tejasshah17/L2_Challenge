import os

cwd = os.getcwd()

data_dir = os.path.join(cwd, 'data')
json_data_path = os.path.join(data_dir, 'json')
csv_data_path = os.path.join(data_dir, 'csv')


def createFolder():
	try:
		if not os.path.exists(data_dir):
			##### -- CREATE JSON & CSV DIRECTORY -- #####
			os.makedirs(json_data_path)
			os.makedirs(csv_data_path)
			return '1', "Data Directory Created Successfully !!"
		return 1, "Folder Exists !!"

	except Exception as ex:
		return -1, repr(ex)