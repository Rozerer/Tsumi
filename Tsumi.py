from selenium import webdriver
import requests 
import time
import telebot
import json

startUrl = 'https://www.instagram.com/accounts/login/'

bot = telebot.TeleBot('812478134:AAE_Tstk_3KDADmwvZUCBFdL-mQNRL1Gx6k')

with open('TsumiUsersDB.json') as json_file:
    data = json.load(json_file)


def get_Photo_Link(url,log,pas):
    
    driver = webdriver.Firefox()

    driver.get(startUrl)

    time.sleep(1.5)

    passwordBar = driver.find_element_by_name('password')
    passwordBar.send_keys(pas)

    loginBar = driver.find_element_by_name('username')
    loginBar.send_keys(log)

    passwordBar.submit()

    time.sleep(1.5)

    driver.get(url)

    time.sleep(1.5)

    try:
        media = [driver.find_element_by_class_name('FFVAD'),'photo']
        res = media[0].get_attribute('srcset')
    except:
        media = [driver.find_element_by_class_name('tWeCl'),'video']
        res = media[0].get_attribute('src')   


    driver.close()

    return res

def get_login(message):
    global login
    login = message.text
    bot.send_message(message.from_user.id, 'Enter your Instagram password')
    bot.register_next_step_handler(message, get_password)

def get_password(message):
    global password
    password = message.text


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == "Привет":
        bot.send_message(message.from_user.id, "Привет, чем я могу тебе помочь?")
    elif message.text == "/start":
        bot.send_message(message.from_user.id, "Hello, my name is Tsumi <3")
        bot.send_message(message.from_user.id, "In order to register your account please enter /reg")
    elif message.text == '/reg':
        bot.send_message(message.from_user.id, "Enter your Instagram login")
        bot.register_next_step_handler(message, get_login) #следующий шаг – функция get_name
    elif message.text == "/help":
        bot.send_message(message.from_user.id, "/reg - your account data")
    else:
        for user in data:
            if user['id'] == str(message.from_user.id):
                login = user['Login']
                password = user['Password']
                bot.send_message(message.from_user.id, get_Photo_Link(message.text,login,password))
            else:
                bot.send_message(message.from_user.id, "Please register first. Use /reg")

bot.polling(none_stop=True, interval=0)