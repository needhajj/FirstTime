# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime, timedelta
import os, os.path
import calendar


year = '1976'
month_range = [x for x in range(1,5)]
m_folder = os.path.join(os.getcwd(), 'Output_Monthly')
n_folder = os.path.join(os.getcwd(), 'OFN')

for month in month_range:
    with open(os.path.join(m_folder, 'Year_'+year+'_'+str(month).zfill(2)+'.csv'), 'r') as csvinput:
        with open(os.path.join(n_folder, 'Year_'+year+'_'+str(month).zfill(2)+'.csv'), 'w+') as csvoutput:
            writer = csv.writer(csvoutput, lineterminator='\n')
            reader = csv.reader(csvinput)
            all_n = []
            for row in reader:
                now = datetime.now()
                row.extend(['eagle.wilco.org', str(now)])
                all_n.append(row)
            writer.writerows(all_n)
            