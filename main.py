# import telebot
# import random
# from telebot import types
# # import speech_recognition as sr
# # from pydub import AudioSegment
# # import os

# API_TOKEN = '7333127473:AAGzpKwddu7iVl-_l6C7bM-bSnGU8Jp_IQ4'

# bot = telebot.TeleBot(API_TOKEN, parse_mode='HTML')



# # Обработчик команды /start
# @bot.message_handler(commands=['start'])
# def send_welcome(message): 
#     #создание клавиатуры 
#     markip = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
#     btn1 = types.KeyboardButton('/help')
#     btn2 = types.KeyboardButton('/rad')
#     markip.add(btn1, btn2)
#     # отправка сообщения юзеру

#     #ответ бота 
#     bot.send_message(message.chat.id, "Добро пожаловать!", reply_markup=markip)

# # Обработчик команды /help
# @bot.message_handler(commands=['help'])
# def send_help(message):
#     help_text = (
#         "<b>Доступные команды:</b>\n"
#         "/start - начать взаимодействие с ботом\n"
#         "/rad - отправить случайное изображение\n"
#         "/help - получить помощь и информацию о командах\n"
#     )
#     bot.reply_to(message, help_text)
# def send_help(messege):
#     bot.reply_to(message)
# # Обработчик команды /rad
# @bot.message_handler(commands=['rad'])
# def send_random_image(message):
    

#     try:
#         # Выбираем случайное число от 0 до 9
#         random_index = random.randint(0, 2)
#         image_path = f"./img/image{random_index}.jpg"
        
#         # Отправляем изображение пользователю
#         with open(image_path, 'rb') as image_file:
#             bot.send_photo(message.chat.id, image_file)
#     except Exception as e:
#         bot.reply_to(message, f"Произошла ошибка: {e}")


# # Обработчик голосовых сообщений
# @bot.message_handler(content_types=['voice'])
# def handle_voice(message):
#     try:
#         file_info = bot.get_file(message.voice.file_id)
#         downloaded_file = bot.download_file(file_info.file_path)

#         voice_ogg_path = "voice.ogg"
#         voice_wav_path = "voice.wav"

#         with open(voice_ogg_path, 'wb') as new_file:
#             new_file.write(downloaded_file)

#         audio = AudioSegment.from_ogg(voice_ogg_path)
#         audio.export(voice_wav_path, format="wav")

#         recognizer = sr.Recognizer()
#         with sr.AudioFile(voice_wav_path) as source:
#             audio_data = recognizer.record(source)
#             text = recognizer.recognize_google(audio_data, language="ru-RU")
#             bot.reply_to(message, f"Вы сказали: {text}")

#         # Удаляем временные файлы
#         os.remove(voice_ogg_path)
#         os.remove(voice_wav_path)
#     except Exception as e:
#         bot.reply_to(message, f"Не удалось распознать голосовое сообщение. Ошибка: {e}")

# # Обработчик входящих изображений
# @bot.message_handler(content_types=['photo', 'video', 'sticker'])
# def handle_image(message):
#     choice = random.choice(['😍', '👍', '👎', 'Ну такое...']) 
#     bot.reply_to(message, choice)

# # Обработчик текстовых сообщений
# @bot.message_handler()
# def handle_unknown_command(message):
#     bot.reply_to(message, "<b>Я не хочу разговаривать на эту тему...</b>")

# # Запуск бота
# bot.polling()






import telebot
import sqlite3


API_TOKEN = "7333127473:AAGzpKwddu7iVl-_l6C7bM-bSnGU8Jp_IQ4"
bot = telebot.TeleBot(API_TOKEN, parse_mode='HTML')

conn = sqlite3.connect('users.db', check_same_thread=False)
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER UNIQUE,
    username TEXT                                                        
    )                           
    ''')
conn.commit()

text_message = ""

@bot.message_handler(commands=["start"])
def send_welkom(message):
    user_id = message.from_user.id 
    username = message.from_user.id


    cursor.execute('''
    SELECT * FROM users WHERE user_id = ?
    ''', (user_id,))
    excepting_user = cursor.fetchone()


    if excepting_user:
        print(f"пользователь {username} уже есть в базе данных!")
    else:
        cursor.execute('''
        INSERT INTO users (user_id, username)
        VALUES (? , ?)                                                                             
        ''', (user_id, username,))
        conn.commit()
        print(f"пользователь {username} успешно добавлен в DB")

    bot.send_message(message.chat.id, "добро пожаловать !")    

@bot.message_handler(commands=['sand'])
def hadle_send(message):
    if message.from_user.id != 1784663884:
        bot.reply_to(message, "у вас нет прав для выполнения этой команды !")
        return
 
    bot.send_message(message.chat.id, 'отправьте техст для рассылки')
    bot.register_next_step_handler(message, process_text)

def process_text(messege):
    global text_message
    text_message = messege.text
    bot.send_message(messege.chat.id, "рассылка началась ->")

    send_broadcast()

def send_broadcast():
    global text_message
    cursor.execute('SELECT user_id FROM users')
    users = cursor.fetchall()

    for user in users:
        user_id = user[0]
        try:
            bot.send_message(user_id, text_message)
        except Exception as e:
            print(f"ошибка с пользователем {user_id}: {e}")

text_message = "" 

@bot.message_handler()
def unkl_command(message):
    if message.text == ".":
        bot.reply_to(message, "а это крутая тема для разговора !")

bot.polling()
