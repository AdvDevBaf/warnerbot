from enum import Enum
import telebot
import logging

class States(Enum):
    """
    Мы используем словарь, в которой храним всегда строковые данные,
    поэтому и тут будем использовать тоже строки (str)
    """
    S_START = "0"  # Начало нового диалога
    S_FIRST_OPTION = '1'
    S_TARGET_GROUP_1 = "2"
    S_TARGET_GROUP_1_PERCENT = "3"
    S_TARGET_GROUP_2 = "4"
    S_TARGET_GROUP_2_PERCENT = "5"
    S_CURRENT_TARGET_GROUP = "6"
    S_SOCIAL_MEDIA_VK = "7"
    S_SOCIAL_MEDIA_VK_SUBSCRIBERS = "8"
    S_SOCIAL_MEDIA_INSTAGRAM= "9"
    S_SOCIAL_MEDIA_INSTAGRAM_SUBSCRIBERS = "10"
    S_SOCIAL_MEDIA_FACEBOOK = "11"
    S_SOCIAL_MEDIA_FACEBOOK_SUBSCRIBERS = "12"
    S_SOCIAL_MEDIA_YOUTUBE = "13"
    S_SOCIAL_MEDIA_YOUTUBE_SUBSCRIBERS = "14"
    S_SOCIAL_MEDIA_TIKTOK = "15"
    S_SOCIAL_MEDIA_TIKTOK_SUBSCRIBERS = "16"
    S_PRODUCT = "17"
    S_PRODUCT_FINALLY = "18"
    S_SOCIAL_MEDIA = "19"
    S_SOCIAL_MEDIA_SUBSCRIBERS = "20"

media_scope_table = {'vkontakte':{'12-17':2,'18-24':2,'25-34': 2, '35-44':1, '45-54':0, '55-64':0, 'М':0, 'Ж':1},
                     'facebook':{'12-17':0,'18-24':0,'25-34': 0, '35-44':1, '45-54':2, '55-64':0, 'М':0, 'Ж':1},
                     'instagram':{'12-17':2,'18-24':2,'25-34': 2, '35-44':1, '45-54':0, '55-64':0, 'М':0, 'Ж':1},
                     'tiktok':{'12-17':2,'18-24':2,'25-34': 2, '35-44':0, '45-54':0, '55-64':0, 'М':0, 'Ж':1},
                     'youtube':{'12-17':1,'18-24':1,'25-34': 1, '35-44':1, '45-54':0, '55-64':0, 'М':1, 'Ж':1}}

media_values = {'vkontakte': 1, 'facebook': 1, 'instagram': 1, 'tiktok': 1, 'youtube': 1}

product_target = {'vkontakte':{'сингл':2, 'альбом/ер':4,'клип':1}, 'facebook':{'сингл':0, 'альбом/ер':1,'клип':0},
           'instagram': {'сингл': 0, 'альбом/ер': 1, 'клип': 1}, 'tiktok':{'сингл':1, 'альбом/ер':1,'клип':1},
           'youtube': {'сингл': 0, 'альбом/ер': 0, 'клип': 10}}

tech_product = {'vkontakte': 2, 'facebook': 0.5, 'instagram': 0.5, 'tiktok': 0, 'youtube': 0}


telegram_bot = telebot.TeleBot('1208714406:AAF8lYlhPcry8Fo6O19uwzOaxSvt3CGgrLo')
keyboard = telebot.types.ReplyKeyboardMarkup(True)
keyboard.row('Start')

keyboard1 = telebot.types.ReplyKeyboardMarkup(True,one_time_keyboard=True)
keyboard1.row('12-17','35-44')
keyboard1.row("18-24","45-54")
keyboard1.row('25-34','55-64')

keyboard2 = telebot.types.ReplyKeyboardMarkup(True)
keyboard2.row('Facebook','Instagram')
keyboard2.row("Vkontakte","Youtube")
keyboard2.row('Tiktok')
keyboard2.row('Дальше')

keyboard3 = telebot.types.ReplyKeyboardMarkup(True)
keyboard3.row('0-50K','300-500K')
keyboard3.row("50-100K","500K+")
keyboard3.row('100-300K')

keyboard4 = telebot.types.ReplyKeyboardMarkup(True)
keyboard4.row('Несколько раз в месяц','Несколько раз в неделю')
keyboard4.row("Раз в неделю","Каждый день")
keyboard4.row("Раз в месяц или реже")

keyboard5 = telebot.types.ReplyKeyboardMarkup(True,one_time_keyboard=True)
keyboard5.row('Сингл','Альбом')
keyboard5.row("ЕР","Клип")

keyboard6 = telebot.types.ReplyKeyboardMarkup(True)
keyboard6.row('Перейти к следующему пункту')

keyboard7 = telebot.types.ReplyKeyboardMarkup(True)
keyboard7.row('Рассчитать')
logging.basicConfig(filename="sample.log", level=logging.INFO)