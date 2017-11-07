# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime, timedelta
import os, os.path
import calendar

# Create the Appropriate Folders
def assure_path_exists(path):
    c_dir = os.path.abspath(path)
    if not os.path.exists(c_dir):
        os.mkdir(c_dir)

assure_path_exists('Output_Annual')
assure_path_exists('Output_Monthly')

# discovering if 'max_pages' is a number
def is_number(self):
    try:
        float(self)
        return True
    except ValueError:
        return False


# Build data range from last file in /Output
list_of_files = os.listdir(os.path.join(os.getcwd(), 'Output_Monthly'))
lof_int = [int(x[5:9]) * 100 + int(x[10:12]) for x in list_of_files]
max_last_date = max(lof_int)
last_yr_str = str(max_last_date / 100)
last_mo_str = str(max_last_date)[4:]
last_fin_day = calendar.monthrange(int(last_yr_str), int(last_mo_str))[1]
last_date_format = datetime.strptime(last_mo_str +'/' + str(last_fin_day) + '/' + last_yr_str, "%m/%d/%Y")
date_1 = last_date_format + timedelta(days=1)
curr_last_day = calendar.monthrange(date_1.year, date_1.month)[1]
date_2 = date_1.replace(day=int(curr_last_day))
date_range = []

for next_date in range(0, int(curr_last_day)):
    date_collect =  date_1 + timedelta(days=next_date)
    date_range.append(str(date_collect.strftime("%m/%d/%Y")))


# Looping through the Dates in the Post search form
table_contents = []
for date_s in date_range:
    if max_last_date == 201705:
        break
    else:
        # Find cookie that bypasses 'Disclaimer'
        cookie_url = 'http://eagle.wilco.org/williamsonweb/session/checkSession'
        search_url = 'https://eagle.wilco.org/williamsonweb/searchPost/DOCSEARCH149S1'
        cookie_request = requests.get(cookie_url)
        cookie_dict = cookie_request.cookies
        required_cookie = dict(requests.utils.dict_from_cookiejar(cookie_dict)).values()[0]
        cookie = { 'JSESSIONID' : str(required_cookie), 'disclaimerAccepted' : 'true' }
        
        input_data = { 'field_BothNamesID-containsInput' :	'Contains+All',
                       'field_GrantorID-containsInput' : 'Contains+All',
                       'field_GranteeID-containsInput' : 'Contains+All',
                       'field_RecDateID-StartDate' : date_s,
                       'field_RecDateID-EndDate' : date_s,
                       'field_selfservice_documentTypes-containsInput' : 'Contains+Any',
        }
        
        rr = requests.post(search_url, params=input_data, cookies=cookie, verify=False)
        
        soup = BeautifulSoup(rr.content, "lxml")
        max_pages_text = soup.find('li', { 'data-role' : "list-divider" }).text
        max_page_lst= max_pages_text.split()
        max_page = max_page_lst[4]
        
        if is_number(max_page) == True:
            max_page_int = int(max_page)
            changing_url = rr.url
            for page_number in range( 1, int(max_page_int) + 1):
                current_url = changing_url[:-1] + str(page_number)
                ind_page = requests.get(url=current_url, cookies=cookie, verify=False)
                soup = BeautifulSoup(ind_page.content, "lxml")
                table = soup.find('table')
                rows = soup.find_all('tr')
                for tr in rows:
                    if rows.index(tr) == 0 : 
                        row_cells = [ th.getText().strip()  for th in tr.find_all('th') if th.getText().strip() != '' ]  
                    else : 
                        row_cells = ([ tr.find('th').getText()  ] if tr.find('th') else [] ) + [ td.getText().strip() for td in tr.find_all('td') if td.getText().strip() != '' ] 
                    if len(row_cells) > 1 :
                        now = datetime.now()
                        row_cells.extend(['eagle.wilco.org', str(now)])
                        table_contents.append(row_cells)


# Rendering in proper code
def fix_unicode(data):
    if isinstance(data, unicode):
        return data.encode('utf-8')
    elif isinstance(data, dict):
        data = dict((fix_unicode(k), fix_unicode(data[k])) for k in data)
    elif isinstance(data, list):
        for i in xrange(0, len(data)):
            data[i] = fix_unicode(data[i])
    return data
table_contents_encoded = fix_unicode(table_contents)


# Setting file name and path
cwd_m = os.getcwd()+'/Output_Monthly'
new_file_name_m = 'Year_' + str(date_1.year) + '_' + str(date_1.month).zfill(2) + '.csv'


# Export as .csv file
with open(os.path.join(cwd_m, new_file_name_m), 'w+') as output:
    writer = csv.writer(output, lineterminator='\n')
    writer.writerows(table_contents_encoded)
print(new_file_name_m)


# Combining individual Month files
# Determine if annual combining is needed
list_of_files_monthly = os.listdir(os.path.join(os.getcwd(), 'Output_Monthly'))
list_of_files_annual = os.listdir(os.path.join(os.getcwd(), 'Output_Annual'))
lofm_int = [int(x[5:9]) for x in list_of_files_monthly if int(x[10:12]) == 12]
lofa_int = [int(x[5:9]) for x in list_of_files_annual]
lofm_set = list(set(lofm_int))


# Looping through matches of unconsolidated years
for un_cons in lofm_set:
    if un_cons not in lofa_int:
        cwd_a = os.getcwd()+'/Output_Annual'
        cwd_m = os.getcwd()+'/Output_Monthly'
        new_file_name_a = 'Year_' + str(un_cons) + '.csv'
        fout = open(os.path.join(cwd_a, new_file_name_a), 'a+')
        
        # Iterate through months    
        for num in range(1,13):
            for line in open(os.path.join(cwd_m, 'Year_'+str(un_cons)+'_'+str(num).zfill(2)+'.csv')):
                fout.write(line)
        fout.close()
        print(new_file_name_a)



# *** Add SSL verification if possible ***
# Ensuring we don't overwrite or duplicate
# Naming sheet additions after months? (if new ones are created rather than appended)
