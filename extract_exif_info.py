from utils.utils import *

def main():
	paths = get_folders('data')
	m = {}

	for path in paths:
		files = get_files_in_path(path)
		datas = get_df(path,files)
		datas = add_rows_direction(datas)
		print('Generating ',path+'exif_row.csv',' ...\t',end='')
		datas.to_csv(path+'exif_row.csv',index=False)
		print('DONE!')

if __name__ == "__main__":
    main()