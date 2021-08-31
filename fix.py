import pandas as pd
import connection
import gspread
from datetime import datetime

df = pd.DataFrame()
def read_table():
    print('Start...')
    global df
    credentials = connection.credentials
    gs = gspread.authorize(credentials)
    work_sheet = gs.open('Schedule')
    sheet1 = work_sheet.sheet1
    data = sheet1.get_all_values()
    headers = data.pop(0)
    df = pd.DataFrame(data, columns=headers)
    return df

df = read_table()
df['Дата и время'] = pd.to_datetime(df['Дата и время'])
current_df = df[(df['Дата и время'].dt.day == datetime.now().day) & (df['Дата и время'].dt.month == datetime.now().month)]

val_list = []
for i in current_df.values:
    now = datetime.now()
    need = i[1]
    arg = str(need - now)[0]
    if arg == '-':
        continue
    else:
        val_list.append(i)
print(val_list)