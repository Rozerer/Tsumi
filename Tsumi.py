import requests
import time
import telebot
import json
import hashlib
import multiprocessing
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options

startUrl = 'https://www.instagram.com/accounts/login/'

token = ''

bot = telebot.AsyncTeleBot(token)

with open('/home/user1/Tsumi/TsumiUsersDB.json') as json_file:
#with open('TsumiUsersDB.json') as json_file:
    data = json.load(json_file)


options = Options()
options.headless = True

def get_Photo_Link(id, url, log, pas):

    #driver = webdriver.Firefox()
    driver = webdriver.Firefox(options=options,executable_path='/home/user1/Tsumi/geckodriver')

    driver.get(startUrl)

    try:
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.NAME, "username")))
    except TimeoutError:
        driver.quit()
        return 'Something went wrong=( Please, try again later.'

    loginBar = driver.find_element_by_name('username')
    loginBar.send_keys(log)

    passwordBar = driver.find_element_by_name('password')
    passwordBar.send_keys(pas)

    passwordBar.submit()

    try:
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, "nwXS6")))
    except TimeoutError:
        driver.quit()
        return 'Something is wrong with your authorization=( Please, try again later.'

    try:
        driver.get(url)
    except:
        driver.quit()
        return 'Something is wrong with your instagram media link=( Please, try again.'

    try:
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, "Kj7h1")))
    except:
        driver.quit()
        return 'Something went wrong=( Please, try again later.'

    try:
        try:
            media = [driver.find_element_by_class_name('FFVAD'), 'photo']
            res = media[0].get_attribute('srcset')
        except:
            media = [driver.find_element_by_class_name('tWeCl'), 'video']
            res = media[0].get_attribute('src')
    except:
        driver.quit()
        return 'Something went wrong=( Please, try again later.'

    driver.quit()

    bot.send_message(id,res)

    return res


def get_login(message):
    global login
    login = message.text
    bot.send_message(message.from_user.id, 'Enter your Instagram password')
    
    bot.register_next_step_handler(message, get_password)


def get_password(message):
    global login
    global password
    password = message.text
    reg_data = {'id': message.from_user.id,
                'Login': login, 'Password': password}
    print(message.from_user.id)
    for user in data:
        if user['id'] == message.from_user.id:
            user['Login'] = login
            user['Password'] = password

            break
    else:
        data.append(reg_data)
    with open('TsumiUsersDB.json', 'w') as json_file_w:
        json.dump(data, json_file_w)


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == "Привет":
        bot.send_message(message.from_user.id,
                         "Hey, how can I help you?")
    elif message.text == "/start":
        bot.send_message(message.from_user.id, "Hello, my name is Tsumi <3")
        bot.send_message(message.from_user.id,
                         "In order to register your account please enter /reg")
    elif message.text == '/reg':
        bot.send_message(message.from_user.id, "Enter your Instagram login")
        bot.register_next_step_handler(message, get_login)
    elif message.text == "/help":
        bot.send_message(message.from_user.id, "/reg - your account data")
    else:
        for user in data:
            if user['id'] == message.from_user.id:   
                t = multiprocessing.Process(target=get_Photo_Link, args=(message.from_user.id, message.text, user['Login'],user['Password'],))
                t.run()
                break
        else:
            bot.send_message(message.from_user.id,
            "Please register first. Use /reg")

bot.polling(none_stop=True, interval=0)
