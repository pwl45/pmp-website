'''import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/spreadsheets",
                 "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name(
    "/etc/config.json", scope)
client = gspread.authorize(creds)
sheet = client.open("PMP Portfolio").get_worksheet(2)
sheet.update('A1','Date') # This line shouldn't be necessary, but updating the sheet makes sure stock prices are live

data = sheet.get_all_records(2)

liszt = list(data)

for l in liszt:
    print(l['Date'],l['Presenter 1'],l['Presenter 2'],l['Presenter 3'],sep='\t')
    #print()'''


import csv

with open('/etc/sched.csv', 'r') as csvfile:
    schedule = csv.reader(csvfile,delimiter=',')

for row in schedule:
    print(row)