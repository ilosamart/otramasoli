import os
from oauth2client.service_account import ServiceAccountCredentials

from config import budget_spreadsheet

scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

credentials = ServiceAccountCredentials.from_json_keyfile_name(
    os.getenv('GOOGLE_CREDENTIALS', 'credentials.json'),
    scope
)

# print(wks)
