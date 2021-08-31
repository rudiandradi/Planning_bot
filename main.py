# Импорт библиотек
import telebot
from datetime import datetime
from threading import Timer
import config
import pandas as pd
import connection
import gspread
import threading
import schedule
import time


# Подключение к боту
bot = telebot.TeleBot(config.TOKEN)

# Отправка сообщений
def send_message(chanel, message):
    bot.send_message(chanel, message, parse_mode='html', disable_web_page_preview=True)

def send_pgoto(chanel, photo):
    bot.send_photo(chanel, photo)

# Чтение таблицы
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

# Создание таймеров
def main():
    global val_list
    val_list = []
    df = read_table()
    df['Дата и время'] = pd.to_datetime(df['Дата и время'])
    current_df = df[(df['Дата и время'].dt.day == datetime.now().day) & (df['Дата и время'].dt.month == datetime.now().month)]
    print('Creating timers...\n')
    for (i, j) in zip(current_df.values, str(range(len(current_df.values)))):

        time = i[1]
        chanel = i[0]
        message = i[2]
        img = i[3]
        now = datetime.now()
        needed = pd.to_datetime([time])

        #### Отсекаем просроченные посты:
        arg = str((needed - now)[0])[0]
        if arg == '-':
            print('Просроченная запись!')
        ###

        else:
            val_list.append([time, chanel, message, img])
            print(f'Время: {time}, Канал: {chanel}, Сообщение: {message}')
            # timer
            print(now.day)
            delta = needed - now

            timer_value_photo = delta.seconds[0] + 4
            j2 = Timer(
                interval=timer_value_photo,
                function=send_pgoto,
                args=[chanel,img]
            )
            j2.start()

            timer_value_text = delta.seconds[0] + 5
            j = Timer(
                interval=timer_value_text,
                function=send_message,
                args=[chanel,message]
            )
            j.start()
            print('Timer successfully created\n')

@bot.message_handler(content_types=['text'])
def mess(message):
    if message.chat.type == 'private':
        if message.text != ' ':
            msg1 = 'Посты на сегодня:\n'
            bot.send_message(message.chat.id, msg1)
            for (i, j) in zip(val_list, range(len(val_list))):
                msg2 = i[3] + '\n<b>Пост №</b><b>' + str(j+1) + '</b>\n<b>Время: </b>' + str(i[0].hour) + ':' + str(i[0].minute) + '\n' + '<b>Канал/чат: </b>' + i[1] + '\n' + '<b>Текст: </b>' + i[2] + '\n\n'
                bot.send_message(message.chat.id,
                                 msg2, parse_mode='html')

main()


def run_bot():
    bot.polling(none_stop=True)
def run():
    schedule.every().day.at("00:05").do(main)
    while True:
        schedule.run_pending()
        time.sleep(1)

e1 = threading.Event()
t1 = threading.Thread(target = run_bot)
t2 = threading.Thread(target=run)
t1.start()
t2.start()
e1.set()
print("Запущено потоков: ", threading.active_count())


