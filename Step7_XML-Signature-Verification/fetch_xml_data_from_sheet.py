import gspread
import csv
import sheetfu
from oauth2client.service_account import ServiceAccountCredentials
from sheetfu import SpreadsheetApp
import json

Gran_file={}
count = 0 

# use creds to create a client to interact with the Google Drive API
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('clients_secret.json', scope)
client = gspread.authorize(creds)

spreadsheet = SpreadsheetApp('clients_secret.json').open_by_id('1KkazipFVA-LLLGi2IlpJmMYnF2TFUKFAyVX5u9Xo5X8')

log_sheets = [
    sheet for sheet in spreadsheet.sheets 
    if sheet.name.startswith("xml_signatures_to_sheet")
]

for log_sheet in log_sheets:
    data_range = log_sheet.get_data_range()
    data2 =[e[0:40] for e in data_range.get_values()]

data2.remove(data2[0])
data2.remove(data2[0])

for row in data2: 
	count= count + 1 
	if count <= 1600:
		if row[1] != "":

			Gran_file[row[0]]= {'app_name':row[1],'GCActivity_Login_Signature_URL':row[10],'GCActivity_Login_Fail_Signature_URL':row[14],
								'GCActivity_Logout_Signature_URL':row[18],'GCActivity_Upload_Signature_URL':row[22],
								'GCActivity_Download_Signature_URL':row[26],'GCActivity_Delete_Signature_URL':row[30],
								'GCActivity_Share_Signature_URL':row[34],'GCActivity_Read-Only_Signature_URL':row[38]
								} 
	if count > 1600:
		break

with open('sheet_data.json', 'w') as fp:  
   json.dump(Gran_file,fp,indent=1)




