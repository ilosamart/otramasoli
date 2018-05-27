import gspread
from oauth2client.service_account import ServiceAccountCredentials

from celeryconfig import budget_spreadsheet

scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

credentials = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)

gc = gspread.authorize(credentials)

sps = gc.open_by_url(budget_spreadsheet)

# sps.add_worksheet('2018-05', 1, 3)

# sps.add_worksheet('2018-06', 1, 3)

wks = sps.worksheet('2018-06')

# print(wks)
