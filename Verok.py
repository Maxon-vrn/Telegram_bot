import telebot
from telebot import types
from PIL import Image
import random 
import config
import os,time,re
import pymysql

bot = telebot.TeleBot(config.TOKEN, parse_mode=None) #доступ к TOKEN переменной в файле config

@bot.message_handler(commands=['start']) #/start or начать - при старте телеги выскакивает, после нажатия выйдет меню бота
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard = True)  #изменение карточек автоматически по размеру окна
    item1 = types.KeyboardButton('чат') # кнопки меню
    item2 = types.KeyboardButton('фото') 
    item3 = types.KeyboardButton('игры')
    item4 = types.KeyboardButton('музыка')
    item5 = types.KeyboardButton('контакты')
    item6 = types.KeyboardButton('развлечения') # развлечения: анекдот, факт, поговорка, комплимент
    
    markup.add(item1,item2,item3,item4,item5,item6)  # добавить кнопки в меню из выше описанных

    bot.send_message(message.chat.id, "Приветствую тебя, {0.first_name}!".format(message.from_user), reply_markup = markup) #передаем marckup
    bot.send_message(message.chat.id,'Выбери интересующую тебя категорию из меню 👇')

@bot.message_handler(content_types = ['text'])
def bot_message(message):
    if message.chat.type == 'private':
        if message.text == 'чат':
            bot.send_message(message.chat.id, "Я пока не умею поддерживать диалог, но скоро научусь!  ;)")

        elif message.text == 'фото':
            markup = types.ReplyKeyboardMarkup(resize_keyboard = True)  #изменение карточек автоматически по размеру окна
            item1 = types.KeyboardButton('кошки') 
            item2 = types.KeyboardButton('собаки') 
            item3 = types.KeyboardButton('автомобили')
            back = types.KeyboardButton('↩ назад') 
            markup.add(item1,item2,item3,back)  # добавить кнопки в меню из выше описанных

            bot.send_message(message.chat.id, "Выбери категорию картинок которую ты хочешь посмотреть 👇", reply_markup = markup) #передаем marckup

        # ----------------- back -----------------    
        elif message.text == '↩ назад':
            markup = types.ReplyKeyboardMarkup(resize_keyboard = True) 
            item1 = types.KeyboardButton('чат') 
            item2 = types.KeyboardButton('фото') 
            item4 = types.KeyboardButton('музыка')
            item6 = types.KeyboardButton('развлечения') #развлечения: анекдот, факт, поговорка, комплимент
            item5 = types.KeyboardButton('контакты')

            markup.add(item1,item2,item4,item5,item6)  # добавить кнопки в меню из выше описанных

            bot.send_message(message.chat.id, "Выбери категорию которую ты хочешь посмотреть 👇", reply_markup = markup)


        
        elif message.text == 'автомобили': 
            # настроено на рандомноую выдачу картинок по запросу(чем больше в папке/директории, тем лучше)
            directory = './photo/cars'
            list = []
            for filename in os.listdir(directory):
                f = os.path.join(directory, filename) # здесь находится директори+имя файла
                list.append(f) # все пути к файлам положили в список
            x = random.choice(list) #выбрали из списка рэндомом путь
            img = Image.open(x)

            bot.send_photo(message.chat.id, img)

        elif message.text == 'кошки': #следующие два имеют ссылки на конкретные файлы
            photo = open('./photo/cat/cat1.jpeg', 'rb')   
            bot.send_photo(message.chat.id, photo)  
        elif message.text == 'собаки':
            photo = open('./photo/dog/dog1.jpeg', 'rb')   
            bot.send_photo(message.chat.id, photo)  


        elif message.text == 'музыка': # .DS_Store  - провести проверку на расширения перед отправкой в чат
            bot.send_message(message.chat.id,'Хит из музыкальных чартов этой недели.')   
            directory = './music/'
            list_music=[]
            for filename in os.listdir(directory): #перебор всех файлов в папке
                #провести проверку на расширения перед отправкой в чат
                if filename.split('.')[-1] == 'mp3':  #проверка на расширение файла mp3 
                    f = os.path.join(directory, filename) # здесь находится директори+имя файла
                    list_music.append(f) #добавили все пути в список
            melodi = random.choice(list_music) #выбрали конкретный путь   
            f = open(melodi, 'rb') # open rendom file at library            
            bot.send_audio(message.chat.id, f) # download music fail client listen
        
        elif message.text == 'контакты': 
            bot.send_message(message.chat.id, "Создан в ознакомительных целях и поднятия настроения!")
            bot.send_message(message.chat.id, "Контактная информация: telegram:@Fisenko_Maxim  т.8-960-101-90-39")
            bot.send_message(message.chat.id, "Во время создания бота - ни одна нервная клетка не пострадала!")
 
               
        elif message.text == 'развлечения':
            markup = types.ReplyKeyboardMarkup(resize_keyboard = True)  #изменение карточек автоматически по размеру окна
            item1 = types.KeyboardButton('факты') 
            item2 = types.KeyboardButton('комплименты') 
            item3 = types.KeyboardButton('анекдоты 18+') # шутка
            item4 = types.KeyboardButton('---') # поговорка
            back = types.KeyboardButton('↩ назад')

            markup.add(item1,item2,item3,item4,back)  # добавить кнопки в меню из выше описанных
            bot.send_message(message.chat.id,'Выбери из меню ниже, что тебе по вкусу',reply_markup = markup) # без передачи 'text' don`t work!!!

        elif message.text == 'факты':
            bot.send_message(message.chat.id, "107 фактов о человеческом теле.")
            f = open('./etc/facts.txt','r',encoding='UTF-8')
            facts = []

            for i in f:
                if i.split() != []:
                    facts.append(i)
            bot.send_message(message.chat.id,random.choice(facts))
        elif message.text == 'комплименты':
            f = open('./etc/compliment.txt','r',encoding='UTF-8')
            facts = []

            for i in f:
                if i.split() != []:
                    facts.append(i)
            bot.send_message(message.chat.id,random.choice(facts))
        elif message.text == 'анекдоты 18+':
            f = open('./etc/anekdotov.txt','r',encoding='UTF-8')
            facts = []

            for i in f:
                if i.split() != []:
                    facts.append(i)
            bot.send_message(message.chat.id,random.choice(facts))    
        elif message.text == 'игры':
            bot.send_message(message.chat.id, "Пока я не обучена играм.")
            bot.send_message(message.chat.id, "Возможно скоро все изменится")

# Handles all sent documents and audio files
@bot.message_handler(content_types=['document', 'audio','video'])
def handle_docs_audio(message):
	bot.send_message(message.chat.id, "Я не умею этим пользоваться. Вернитесь в основное меню - /start.") #передаем marckup


@bot.message_handler(commands=['music']) # на вход получаем команду /music
def find_file_ids(message):
    bot.send_message(message.chat.id,'Хит из музыкальных чартов этой недели.')   
    directory = './music/'
    list_music=[]
    for filename in os.listdir(directory): #перебор всех файлов в папке
        #провести проверку на расширения перед отправкой в чат
        if filename.split('.')[-1] == 'mp3':  #проверка на расширение файла mp3 
            f = os.path.join(directory, filename) # здесь находится директори+имя файла
            list_music.append(f) #добавили все пути в список
            melodi = random.choice(list_music) #выбрали конкретный путь   
            f = open(melodi, 'rb') # open rendom file at library            
            bot.send_audio(message.chat.id, f) # download music fail client listen







#if __name__ == '__main__':
#    bot.polling(none_stop=True, interval=0)   #запуск цикла обработки сообщений 
bot.polling(none_stop=True)      