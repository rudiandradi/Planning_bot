from connection import spreadsheetId
import apiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials
import httplib2

CREDENTIALS_FILE = 'nikolaev.json'
credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive'])
httpAuth = credentials.authorize(httplib2.Http()) # Авторизуемся в системе
service = apiclient.discovery.build('sheets', 'v4', http = httpAuth) # Выбираем работу с таблицами и 4 версию API
driveService = apiclient.discovery.build('drive', 'v3', http = httpAuth)
access = driveService.permissions().create(
    fileId = spreadsheetId,
    body = {'type': 'user', 'role': 'writer', 'emailAddress': 'tier.azazel@gmail.com'},  # Открываем доступ на редактирование
    fields = 'id'
).execute()