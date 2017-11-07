import requests
from bs4 import BeautifulSoup
import csv
import json
from datetime import datetime, timedelta
import glob
import os, os.path

aa = os.listdir('/home/ubuntu/workspace/williamson/williamson/spiders/Output')
bb = [x[5:7] for x in aa]
cc = [x[8:12] for x in aa]
print(int(bb[0]), int(cc[0]))

'''
cwd = os.getcwd()+'/Output'
print(cwd)
year = '10/20/2017'
new_file_name = 'Year_' + year[-4:] + '.csv'
print(new_file_name)

with open(os.path.join(cwd, new_file_name), 'wb') as file1:
    toFile = "Write what you want into the field"
    file1.write(toFile)
'''
'''
start_date_str = '1975/01/01'
date_1 = datetime.strptime(start_date_str, "%Y/%m/%d")
date_2 = datetime.strptime(start_date_str[:4]+'12/31', "%Y/%m/%d")
date_range = []
while date_1 <= date_2:
    date_collect = date_1.strftime("%m/%d/%Y")
    date_range.append(str(date_collect))
    date_1 += timedelta(days=1)
'''
