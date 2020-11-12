from Settings import *


bot = telegram_bot

state = {}
social_media_list = []
ages = dict()
media_name = {}

def get_current_state(user_id):
    try:
        return state[user_id]
    except KeyError as ex:  # Если такого ключа почему-то не оказалось
        logging.error(ex.args[0])
        return States.S_START.value

@bot.message_handler(commands=['start'])
def start_message(message):
    state[message.chat.id] = States.S_START.value
    bot.send_message(message.chat.id,'Привет! Я бот Warner Music Russia, помогу определить эффективный медиа микс для '
                                     'продвижения артиста. Для того, чтобы рассчитать медиа микс за 5 минут, '
                                     'скорее нажимай Start, или напиши команду /startestimation', reply_markup=keyboard)

@bot.message_handler(commands=['reset'])
def set_reset(message):
    state[message.chat.id] = States.S_START.value
    bot.send_message(message.chat.id, 'OK', reply_markup=keyboard)


@bot.message_handler(commands=['help'])
def get_help(message):
    c = ('/start' ,'/startestimation' ,'/help', '/reset')
    bot.send_message(message.chat.id,'Список команд: \n'
                                     '' + str(c[0]) + ' - Запуск бота\n'
                                     '' + str(c[1]) + ' - Начать работу с ботом\n'
                                     '' + str(c[2]) + ' - Запросить список команд\n'
                                     '' + str(c[3]) + ' - Сброс к началу диалога\n',reply_markup=keyboard)


@bot.message_handler(func=lambda message: get_current_state(message.chat.id) == States.S_FIRST_OPTION.value)
@bot.message_handler(commands=['startestimation'])
def target_group_1(message):
    if message.text.lower() in list(media_scope_table['vkontakte'].keys()):
        for item in list(media_scope_table.keys()):
            ages[item] = {message.text.lower():media_scope_table[item][message.text.lower()]}
        state[message.chat.id] = States.S_TARGET_GROUP_1.value
        bot.send_message(message.chat.id, 'Укажи процент данной аудитории среди фанатов артиста? Например, 43%. '                                          'Эту информацию можно посмотреть в профиле соц групп артиста ')
    else:
        bot.send_message(message.chat.id, 'Кто текущая аудитория артиста? '
                                          'Выбери две возрастных категории в порядке приоритета',
                         reply_markup=keyboard1)
        state[message.chat.id] = States.S_FIRST_OPTION.value



@bot.message_handler(func=lambda message: get_current_state(message.chat.id) == States.S_TARGET_GROUP_1.value)
def target_group_1_percent(message):
    if '%' in message.text.lower():
        for i,v in enumerate(ages):
            if int(message.text.lower().replace('%','')) > 50:
                ages[v]['percent_1'] =  media_scope_table[v][list(ages[v].keys())[0]]
            elif 25 < int(message.text.lower().replace('%','')) < 50:
                ages[v]['percent_1'] =  media_scope_table[v][list(ages[v].keys())[0]]/2
            else:
                ages[v]['percent_1'] = 0
        state[message.chat.id] = States.S_TARGET_GROUP_1_PERCENT.value
        bot.send_message(message.chat.id, 'Кто текущая аудитория артиста? Укажи вторую по приоритету группу',
                         reply_markup=keyboard1)
    else:
        bot.send_message(message.chat.id,
                             'Похоже, ты забыл добавить % в конце числа. Попробуй еще раз')

@bot.message_handler(func=lambda message: get_current_state(message.chat.id) == States.S_TARGET_GROUP_1_PERCENT.value)
def target_group_2(message):
    if message.text.lower() in list(media_scope_table['vkontakte'].keys()):
        if message.text.lower() not in dict(ages.values()).keys():
            for item in list(media_scope_table.keys()):
                ages[item][message.text.lower()] = media_scope_table[item][message.text.lower()]
            state[message.chat.id] = States.S_TARGET_GROUP_2.value
            bot.send_message(message.chat.id, 'Укажи процент данной аудитории среди фанатов артиста?')
        else:
            bot.send_message(message.chat.id, 'Ой, такая уже выбрана. Выбери другую',
                             reply_markup=keyboard1)
            state[message.chat.id] = States.S_TARGET_GROUP_1_PERCENT.value
    else:
        bot.send_message(message.chat.id, 'Кто текущая аудитория артиста? Укажи вторую по приоритету группу',
                         reply_markup=keyboard1)


@bot.message_handler(func=lambda message: get_current_state(message.chat.id) == States.S_TARGET_GROUP_2.value)
def target_group_2_percent(message):
    if '%' in message.text.lower():
        for i,v in enumerate(ages):
            if int(message.text.lower().replace('%','')) > 50:
                ages[v]['percent_2'] =  media_scope_table[v][list(ages[v].keys())[2]]
            elif 25 < int(message.text.lower().replace('%','')) < 50:
                ages[v]['percent_2'] =  media_scope_table[v][list(ages[v].keys())[2]]/2
            else:
                ages[v]['percent_2'] = 0
        logging.info(ages)
        state[message.chat.id] = States.S_TARGET_GROUP_2_PERCENT.value
        bot.send_message(message.chat.id, 'Кто текущая аудитория артиста? Укажи,'
                                          'сколько % мужской аудитории и сколько женской,'
                                          'например, вот так 40,60')
    else:
        bot.send_message(message.chat.id,
                             'Похоже, ты забыл добавить % в конце числа. Попробуй еще раз')


@bot.message_handler(func=lambda message: get_current_state(message.chat.id) == States.S_TARGET_GROUP_2_PERCENT.value)
def current_target_group_percent(message):
    state[message.chat.id] = States.S_CURRENT_TARGET_GROUP.value
    temporary = message.text.lower().split(',')
    for i,v in enumerate(ages):
        if int(temporary[0]) > 60:
            ages[v]['M'] =  media_scope_table[v]['М']
        elif 25 < int(temporary[0]) < 60:
            ages[v]['M'] =  media_scope_table[v]['М']/2
        else:
            ages[v]['M'] = 0

        if int(temporary[1]) > 60:
            ages[v]['W'] =  media_scope_table[v]['Ж']
        elif 25 < int(temporary[1]) < 60:
            ages[v]['W'] =  media_scope_table[v]['Ж']/2
        else:
            ages[v]['W'] = 0

    for elem in list(ages.keys()):
        logging.info((((ages[elem]['percent_1']+ages[elem]['percent_2']) * 0.8) + ((ages[elem]['M']+ages[elem]['W'])*0.2))*0.3)
        ages[elem]['target'] = round((((ages[elem]['percent_1']+ages[elem]['percent_2']) * 0.8) + ((ages[elem]['M']+ages[elem]['W'])*0.2))*0.3,2)

    print(ages)
    logging.info(ages)
    #final_data.append(((sum(list(ages.values())) * 0.8) + (sum(man_women)*0.2))*0.3)
    bot.send_message(message.chat.id, 'ok', reply_markup=keyboard6)


@bot.message_handler(func=lambda message: get_current_state(message.chat.id) == States.S_CURRENT_TARGET_GROUP.value)
def social_media(message):
    if message.text.lower() == 'vkontakte':
        #state[message.chat.id] = States.S_SOCIAL_MEDIA_VK.value
        if str(message.text).lower() not in social_media_list:
            social_media_list.append(str(message.text).lower())
            bot.send_message(message.chat.id, message.text +' добавлена для отслеживания',
                             reply_markup=keyboard2)
            logging.info(message.text + str(' добавлена для отслеживания'))
        else:
            social_media_list.remove(str(message.text).lower())
            bot.send_message(message.chat.id, message.text + ' убрана из отслеживания',
                             reply_markup=keyboard2)
            logging.info(message.text + str(' убрана из отслеживания'))
    elif message.text.lower() == 'instagram':
        #state[message.chat.id] = States.S_SOCIAL_MEDIA_INSTAGRAM.value
        if str(message.text).lower() not in social_media_list:
            social_media_list.append(str(message.text).lower())
            bot.send_message(message.chat.id, message.text + ' добавлена для отслеживания',
                             reply_markup=keyboard2)
            logging.info(message.text + str(' добавлена для отслеживания'))
        else:
            social_media_list.remove(str(message.text).lower())
            bot.send_message(message.chat.id, message.text + ' убрана из отслеживания',
                             reply_markup=keyboard2)
            logging.info(message.text + str(' убрана из отслеживания'))
    elif message.text.lower() == 'facebook':
        #state[message.chat.id] = States.S_SOCIAL_MEDIA_FACEBOOK.value
        if str(message.text).lower() not in social_media_list:
            social_media_list.append(str(message.text).lower())
            bot.send_message(message.chat.id, message.text + ' добавлена для отслеживания',
                             reply_markup=keyboard2)
            logging.info(message.text + str(' добавлена для отслеживания'))
        else:
            social_media_list.remove(str(message.text).lower())
            bot.send_message(message.chat.id, message.text + ' убрана из отслеживания',
                             reply_markup=keyboard2)
            logging.info(message.text + str(' убрана из отслеживания'))
    elif message.text.lower() == 'youtube':
        #state[message.chat.id] = States.S_SOCIAL_MEDIA_YOUTUBE.value
        if str(message.text).lower() not in social_media_list:
            social_media_list.append(str(message.text).lower())
            bot.send_message(message.chat.id, message.text + ' добавлена для отслеживания',
                             reply_markup=keyboard2)
            logging.info(message.text + str(' добавлена для отслеживания'))
        else:
            social_media_list.remove(str(message.text).lower())
            bot.send_message(message.chat.id, message.text + ' убрана из отслеживания',
                             reply_markup=keyboard2)
            logging.info(message.text + str(' убрана из отслеживания'))
    elif message.text.lower() == 'tiktok':
        #state[message.chat.id] = States.S_SOCIAL_MEDIA_TIKTOK.value
        if str(message.text).lower() not in social_media_list:
            social_media_list.append(str(message.text).lower())
            bot.send_message(message.chat.id, message.text + ' добавлена для отслеживания',
                             reply_markup=keyboard2)
            logging.info(message.text + ' добавлена для отслеживания')
        else:
            social_media_list.remove(str(message.text).lower())
            bot.send_message(message.chat.id, message.text + ' убрана из отслеживания',
                             reply_markup=keyboard2)
            logging.info(message.text + str(' убрана из отслеживания'))
    elif message.text.lower() == 'дальше':
        state[message.chat.id] = States.S_SOCIAL_MEDIA.value
        bot.send_message(message.chat.id, 'Сколько подписчиков на ' + str(social_media_list[0]) +
                         ' суммарно на личной странице и в официальном сообществе артиста?', reply_markup=keyboard3)
    else:
        bot.send_message(message.chat.id, 'В каких соц сетях есть личная страничка или сообщество артиста?',
                         reply_markup=keyboard2)
    for social_medias in social_media_list:
        if message.text.lower() != 'дальше':
            if message.text.lower() in social_medias:
                # media_name[message.text.lower()] = 1
                media_name[message.text.lower()] = {'value': 1, 'target': ages[message.text.lower()]['target']}
            else:
                media_name[message.text.lower()] = {'value': 0, 'target': ages[message.text.lower()]['target']}

@bot.message_handler(func=lambda message: get_current_state(message.chat.id) == States.S_SOCIAL_MEDIA.value)
def social_media_subscribers(message):
    posting = {'0-50k': 49000, '50-100k': 99000, '100-300k': 299000, '300-500k': 499000, '500k+': 500001}
    if message.text.lower() in list(posting.keys()):
        if posting[message.text.lower()] > 500000:
            media_name[social_media_list[0]]['subs'] = media_name[social_media_list[0]]['value']*3
        elif 300000 <= posting[message.text.lower()] <= 500000:
            media_name[social_media_list[0]]['subs'] = media_name[social_media_list[0]]['value']*2
        elif 99000 <= posting[message.text.lower()] <= 300000:
            media_name[social_media_list[0]]['subs'] = media_name[social_media_list[0]]['value']
        else:
            media_name[social_media_list[0]]['subs'] = 0
        state[message.chat.id] = States.S_SOCIAL_MEDIA_SUBSCRIBERS.value
        bot.send_message(message.chat.id,
                         'Как часто публикуется контент на странице артиста в ' + social_media_list[0] + ' ?',
                         reply_markup=keyboard4)

@bot.message_handler(func=lambda message: get_current_state(message.chat.id) == States.S_SOCIAL_MEDIA_SUBSCRIBERS.value)
def social_media_data(message):
    if message.text.lower() == 'каждый день':
        media_name[social_media_list[0]]['post'] = media_name[social_media_list[0]]['value'] * 3
    elif message.text.lower() == 'несколько раз в неделю':
        media_name[social_media_list[0]]['post'] = media_name[social_media_list[0]]['value'] * 2
    elif message.text.lower() == 'раз в неделю':
        media_name[social_media_list[0]]['post'] = media_name[social_media_list[0]]['value']
    else:
        media_name[social_media_list[0]]['post'] = 0

    social_media_list.remove(social_media_list[0])
    if not social_media_list:
        state[message.chat.id] = States.S_PRODUCT.value
        for elem in list(media_name.keys()):
            logging.info(((media_name[elem]['value']*0.35) + (media_name[elem]['subs']*0.4) + (media_name[elem]['post']*0.25))*0.2)
            media_name[elem]['media'] = round(((media_name[elem]['value']*0.35) +
                                              (media_name[elem]['subs']*0.4) +
                                              (media_name[elem]['post']*0.25))*0.2,2)
        logging.info(media_name)
        bot.send_message(message.chat.id, 'Какой продукт сейчас необходимо продвинуть? ',
                         reply_markup=keyboard5)
    else:
        bot.send_message(message.chat.id, 'Сколько подписчиков на ' + str(social_media_list[0]) +
                         ' суммарно на личной странице и в официальном сообществе артиста?', reply_markup=keyboard3)
        state[message.chat.id] = States.S_SOCIAL_MEDIA.value


@bot.message_handler(func=lambda message: get_current_state(message.chat.id) == States.S_PRODUCT.value)
def product(message):
    prod = {}
    for item in list(media_name.keys()):
        if message.text.lower() in ('сингл', 'альбом/ер', 'клип'):
            prod[item] = product_target[item][message.text.lower()]
        else:
            prod[item] = 0
    for elem in list(prod.keys()):
        media_name[elem]['prod'] = prod[elem]*0.3
    state[message.chat.id] = States.S_PRODUCT_FINALLY.value
    bot.send_message(message.chat.id, 'Почти готово. Рассчитать?',
                     reply_markup=keyboard6)

@bot.message_handler(func=lambda message: get_current_state(message.chat.id) == States.S_PRODUCT_FINALLY.value)
def product_value(message):
    media_mix = {'facebook':0,'vkontakte':0,'instagram':0,'tiktok':0,'youtube':0}
    for i,v in enumerate(media_name):
        print(media_name[v]['target']+media_name[v]['media']+media_name[v]['prod']+tech_product[v])
        if media_name[v]['target']+media_name[v]['media']+media_name[v]['prod']+tech_product[v] < 1:
            media_mix[v] = 0
        else:
            media_mix[v] = media_name[v]['target']+media_name[v]['media']+media_name[v]['prod']+tech_product[v]
    bot.send_message(message.chat.id,'Алгоритм рассчитал эффективный медиа микс для артиста:\n'
    'Vk.com ' + str(round(media_mix['vkontakte'] / (sum(list(media_mix.values()))) * 100)) + '%\n'
    'Facebook ' + str(round(media_mix['facebook'] / (sum(list(media_mix.values()))) * 100)) + '%\n'
    'Instagram ' + str(round(media_mix['instagram'] / (sum(list(media_mix.values()))) * 100)) + '%\n'
    'YouTube ' + str(round(media_mix['youtube'] / (sum(list(media_mix.values()))) * 100)) + '%\n'
    'Tiktok ' + str(round(media_mix['tiktok'] / (sum(list(media_mix.values()))) * 100)) + '%\n'
    'Примените указанные проценты к медиа бюджету. '
    'Подобрать эффективные таргетинги вам поможет ваш личный менеджер в агентстве UM',reply_markup=keyboard)
    logging.error('Алгоритм рассчитал эффективный медиа микс для артиста:\n'
    'Vk.com ' + str(round(media_mix['vkontakte'] / (sum(list(media_mix.values()))) * 100)) + '%\n'
    'Facebook ' + str(round(media_mix['facebook'] / (sum(list(media_mix.values()))) * 100)) + '%\n'
    'Instagram ' + str(round(media_mix['instagram'] / (sum(list(media_mix.values()))) * 100)) + '%\n'
    'YouTube ' + str(round(media_mix['youtube'] / (sum(list(media_mix.values()))) * 100)) + '%\n'
    'Tiktok ' + str(round(media_mix['tiktok'] / (sum(list(media_mix.values()))) * 100)) + '%\n'
    'Примените указанные проценты к медиа бюджету. '
    'Подобрать эффективные таргетинги вам поможет ваш личный менеджер в агентстве UM')
    if message.text.lower() == 'start':
        state[message.chat.id] = States.S_FIRST_OPTION.value
        bot.send_message(message.chat.id, 'Кто текущая аудитория артиста? '
                                          'Выбери две возрастных категории в порядке приоритета',
                         reply_markup=keyboard1)

@bot.message_handler(content_types=['text'])
def send_text(message):
    if message.text.lower() == 'start':
        state[message.chat.id] = States.S_FIRST_OPTION.value
        target_group_1(message)
    else:
        bot.send_message(message.chat.id, 'Прости, я тебя не понимаю. Отправь мне /help, если тебе требуется помощь')

bot.polling()