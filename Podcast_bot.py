import telebot
from yt_dlp import YoutubeDL
import random
from Podcast_bot_message import welcome_message, comands_dict, base_anecdote, url_error

bot = telebot.TeleBot('TOKEN')    #Ваш токен телеграмм бота


@bot.message_handler(commands=['start'])    #Бот приветствует пользователся
def start(message):
  bot.send_message(message.chat.id, welcome_message)


@bot.message_handler(commands=['author'])   #Команда, отправляющая пользователю ссылку на профиль создателя бота
def author(message):
  bot.send_message(message.chat.id, comands_dict['author'])


@bot.message_handler(commands=['help'])     #Команда, отправляющая сообщение с объяснением работы бота
def help(message):
  bot.send_message(message.chat.id, comands_dict['help'])


@bot.message_handler(commands=['GitHub_Directory'])     #Команда, отправляющая ссылку на директория бота на GitHub
def github(message):
  bot.send_message(message.chat.id, comands_dict['GitHub_Directory'])


def Song(song_url, song_title):     #Формат URL ссылка
  outtmpl = song_title + '.%(id)s'
  ydl_opts = {
      'format': 'bestaudio/best',
      'outtmpl': outtmpl,
      'postprocessors': [
          {'key': 'FFmpegExtractAudio','preferredcodec': 'mp3',
           'preferredquality': '192',
          },
          {'key': 'FFmpegMetadata'},
      ],
  }
  with YoutubeDL (ydl_opts) as ydl:
      ydl.download([song_url])      #Скачивание видео в виде mp3 файла


@bot.message_handler(content_types=['text'])
def download(message):
    '''#Функция принимает URL ссылку в виде текстового сообщения и обрабатывает её'''
    try:
        if 'www.youtube.com/watch?v=' in message.text:
            number_1 = random.randint(1, 20)
            bot.reply_to(message, base_anecdote[number_1])    #Бот отправляет один из двадцети анекдотов
            song_url_1 = message.text   #Переменная, которая содержит URL ссылку
            song_url_1 = song_url_1.split('watch?v=')[-1]
            Song(song_url_1, f'{song_url_1}')   #Обработка переменной функцией Song
            audio_1 = open(rf"{song_url_1}.mp3", 'rb')
            bot.send_audio(message.chat.id, audio_1)    #Отправка mp3 файла
            audio_1.close()
        elif 'youtu.be' in message.text:
            number_2 = random.randint(1, 20)
            bot.reply_to(message, base_anecdote[number_2])  # Бот отправляет один из двадцети анекдотов
            song_url_2 = message.text.replace('youtu.be/', 'www.youtube.com/watch?v=')    #превращение ссылки в нужный формат
            song_url_2 = song_url_2.split('watch?v=')[-1]
            Song(song_url_2, f'{song_url_2}')   #Обработка переменной функцией Song
            audio = open(rf"{song_url_2}.mp3", 'rb')
            bot.send_audio(message.chat.id, audio)     #Отправка mp3 файла
            audio.close()
    except:     #Обработка ошибки
        number_3 = random.randint(1, 4)
        bot.send_message(message.chat.id, url_error[number_3])   #Отправка одного из четырёх сообщений в случае ошибки

bot.polling()