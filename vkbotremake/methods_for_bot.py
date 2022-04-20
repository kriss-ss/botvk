import json
from random import randint, choice
import pymorphy2
# import wikipedia
# from gtts import gTTS
# from pprint import pprint
import requests
from vk_api import VkApi
import datetime as dt
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from time import sleep


# def send_message(peer_id, message):  # отправка сообщения
#     peer_id = int(peer_id)
#     try:
#         vk.messages.send(
#             peer_id=peer_id,
#             message=message,
#             random_id=randint(0, 1000000000),
#         )
#     except Exception:
#         return 0


# def new(peer_id):  # проверка беседы
#     peer_id = str(peer_id)
#     with open('list_of_conversations.json') as f:
#         sp = json.load(f)
#     if peer_id in sp:  # если такая беседа уже была, то ничего не делается
#         return 0
#     sp.append(peer_id)  # если этой беседы ещё не было, то создаётся json файл со словарём
#     with open('list_of_conversations.json', 'w') as f:
#         f.write(json.dumps(sp, ensure_ascii=False))
#     sl = {'names': {}, 'can_send_weather': True, 'can_send_random': True,
#           'can_change_nik': True, 'static_for_random': {}, 'list_id': [], 'title': 'натуралом', 'subjects': {},
#           'play_in_zeros': {}, 'waiting_for_confirmation': {}, 'plaing_in_zeros': {}, 'in_zeros': {}}
#     try:
#         list_of_people = vk.messages.getConversationMembers(peer_id=peer_id)
#         for people in list_of_people['profiles']:
#             sl['list_id'].append(str(people['id']))
#             sl['names'][str(people['id'])] = people['first_name'] + " " + people['last_name']
#             sl['play_in_zeros'][str(people['id'])] = 0
#             sl['static_for_random'][str(people['id'])] = 0
#         with open('conversations.json') as f:
#             sp228 = json.load(f)
#         sp228[peer_id] = sl
#         with open('conversations.json', 'w') as f:
#             f.write(json.dumps(sp228, ensure_ascii=False))
#     except Exception:
#         send_message(peer_id, 'Пожалуйста, сделайте бота админом')


# def change_nik(peer_id, user_id, new_name):  # смена ника
#     peer_id = str(peer_id)
#     user_id = str(user_id)
#     with open('conversations.json') as f:
#         sl = json.load(f)
#     if not sl[peer_id]['can_change_nik']:
#         send_message(peer_id, 'Смена ника в беседе запрещена')
#     sl[peer_id]['names'][user_id] = new_name
#     send_message(peer_id, 'Ok')
#     with open('conversations.json', 'w') as f:
#         f.write(json.dumps(sl, ensure_ascii=False))


# def check_people(peer_id, user_id):  # проверка был ли человек в это беседе и раньше
#     peer_id = str(peer_id)  # надо переделать, чтобы вызывалась только при определённом event
#     user_id = str(user_id)
#     with open('conversations.json') as f:
#         sl = json.load(f)
#     new_sl = {}
#     if user_id not in sl[peer_id]['list_id']:
#         sl[peer_id]['list_id'].append(user_id)
#         list_of_people = vk.messages.getConversationMembers(peer_id=peer_id)
#         for people in list_of_people['profiles']:
#             if str(people['id']) in sl[peer_id]['names']:
#                 new_sl[str(people['id'])] = sl[peer_id]['names'][str(people['id'])]
#             else:
#                 new_sl[str(people['id'])] = people['first_name'] + " " + people['last_name']
#                 sl[peer_id]['static_for_random'][str(people['id'])] = 0
#                 sl[peer_id]['list_id'].append(str(people['id']))
#                 sl[peer_id]['play_in_zeros'][str(people['id'])] = 0
#         sl[peer_id]['names'] = new_sl
#     with open('conversations.json', 'w') as f:
#         f.write(json.dumps(sl, ensure_ascii=False))


# def random_user(peer_id):  # функция для рандомного выбора
#     peer_id = str(peer_id)
#     with open('conversations.json') as f:
#         sl = json.load(f)
#     if sl[peer_id]['can_send_random']:
#         random_id = str(choice(sl[peer_id]['list_id']))
#         sl[peer_id]['static_for_random'][random_id] += 1
#         send_message(peer_id,
#                      'Сегодня ' + sl[peer_id]['title'] + ' становится: [id' + random_id + '|' + sl[peer_id]['names'][
#                          random_id] + ']')
#     else:
#         send_message(peer_id, 'Команда в этой беседе запрещена')
#     with open('conversations.json', 'w') as f:
#         f.write(json.dumps(sl, ensure_ascii=False))


# def get_static(peer_id):  # функция для выдачи статистики
#     peer_id = str(peer_id)
#     with open('conversations.json') as f:
#         sl = json.load(f)
#     message = ''
#     for user_id in sl[peer_id]['static_for_random']:
#         message += '[id' + user_id + '|' + sl[peer_id]['names'][user_id] + ']: ' + str(
#             sl[peer_id]['static_for_random'][user_id]) + '\n'
#     send_message(peer_id, message)


# def change_nik_from(user_id, peer_id, nik):  # функция по смене ника
#     peer_id = str(peer_id)
#     with open('conversations.json') as f:
#         sl = json.load(f)
#     if not sl[peer_id]['can_change_nik']:
#         send_message(peer_id, 'Команда запрещена в этой беседе')
#     elif len(nik) > 54:
#         # send_message(peer_id, 'Иди нахрен, Влад')
#         send_message(peer_id, 'Ограничение по длине - 50 символов')
#     elif nik[0:5] != '+ник ':
#         return 0
#     else:
#         change_nik(peer_id, user_id, nik[5::])


# def from_second_to_date(ts):  # перевод из секунд в дату
#     return dt.datetime.utcfromtimestamp(ts)


# def get_weather_days(num):  # отправляет API запрос для погоды и преобразует его в удобную форму
#     response = requests.get(ur)
#     weather = response.json()
#     res_weather = {}
#     for n in range(num):
#         res_weather[str(n) + 'temp_evening'] = int(weather['daily'][n]['temp']['eve'] - 273.15)
#         res_weather[str(n) + 'temp_morning'] = int(weather['daily'][n]['temp']['morn'] - 273.15)
#         res_weather[str(n) + 'temp_night'] = int(weather['daily'][n]['temp']['night'] - 273.15)
#         res_weather[str(n) + 'temp_afternoon'] = int(weather['daily'][n]['temp']['day'] - 273.15)
#         res_weather[str(n) + 'feels_temp_evening'] = int(
#             weather['daily'][n]['feels_like']['eve'] - 273.15)
#         res_weather[str(n) + 'feels_temp_morning'] = int(
#             weather['daily'][n]['feels_like']['morn'] - 273.15)
#         res_weather[str(n) + 'feels_temp_night'] = int(
#             weather['daily'][n]['feels_like']['night'] - 273.15)
#         res_weather[str(n) + 'feels_temp_afternoon'] = int(
#             weather['daily'][n]['feels_like']['day'] - 273.15)
#         res_weather[str(n) + 'wind_speed'] = int(weather['daily'][n]['wind_speed'])
#         res_weather[str(n) + 'date'] = int(weather['daily'][n]['dt'])
#         res_weather[str(n) + 'id'] = weather['daily'][0]['weather'][0]['icon']
#         res_weather[str(n) + 'clouds'] = weather['daily'][n]['weather'][0]['description']
#     return res_weather


# def get_weather_to_some_days(peer_id,
#                              num):  # возращает сообщение с погодой на определённое число дней
#     messag = ''
#     weather = get_weather_days(num)
#     for i in range(num):
#         date = str(from_second_to_date(weather[str(i) + 'date']))[:-8]
#         messag += 'Погода на {}\n\n' \
#                   'Днём {}°, ощущается как {}°\n' \
#                   'Ночью {}°, ощущается как {}°\n' \
#                   'Будет {}\n' \
#                   'Ветер {} М/С\n\n\n'.format(date,
#                                               weather[
#                                                   str(i) + 'temp_afternoon'],
#                                               weather[str(
#                                                   i) + 'feels_temp_afternoon'],
#                                               weather[str(i) + 'temp_night'],
#                                               weather[str(
#                                                   i) + 'feels_temp_night'],
#                                               weather[str(i) + 'clouds'],
#                                               weather[str(i) + 'wind_speed'])
#     send_message(peer_id, messag)


# def get_weather_to_tomorrow(peer_id):  # возращает сообщение с погодой на завтра
#     weather = get_weather_days(2)
#     i = 1
#     date = str(from_second_to_date(weather[str(i) + 'date']))[:-8]
#     messag = ''
#     messag += 'Погода на {}\n\n' \
#               'Днём {}°, ощущается как {}°\n' \
#               'Ночью {}°, ощущается как {}°\n' \
#               'Будет {}\n' \
#               'Ветер {} М/С\n\n\n'.format(date,
#                                           weather[
#                                               str(i) + 'temp_afternoon'],
#                                           weather[str(
#                                               i) + 'feels_temp_afternoon'],
#                                           weather[str(i) + 'temp_night'],
#                                           weather[str(
#                                               i) + 'feels_temp_night'],
#                                           weather[str(i) + 'clouds'],
#                                           weather[str(i) + 'wind_speed'])
#     send_message(peer_id, messag)


#def get_weather(peer_id,
#                message):  # эта функция обрабатывает сообщение с погодой и вызывает различные функции
#    peer_id = str(peer_id)
#    with open('conversations.json') as f:
#        sl = json.load(f)
#    if not sl[peer_id]['can_send_weather']:
#        send_message(peer_id, 'Команда в этой беседе запрещена')
#        return 0
#    if message == 'погода' or message == 'Погода на сегодня':
#        get_weather_to_some_days(peer_id, 1)
#        return 0
#    elif message == 'погода на завтра' or message == 'погода на завтро':
#        get_weather_to_tomorrow(peer_id)
#        return 0
#    message = message.split()
#    if len(message) > 2:
#        if message[2].isdigit():
#            num = int(message[2])
#            if num > 8:
#                send_message(peer_id, 'Слишком большое количество дней')
#            elif num < 1:
#                send_message(peer_id, 'Слишком маленькое количество дней')
#            else:
#                get_weather_to_some_days(peer_id, num)
#        else:
#            send_message(peer_id, 'Не правильный формат ввода')
#    else:
#        send_message(peer_id, 'Ошибка')


# def change_settings(peer_id, message):  # обрабатывает изменение настроек
#     peer_id = str(peer_id)
#     message = message.split()
#     if message[0] == '+setting' and len(message) > 2:
#         print(message)
#         try:
#             with open('conversations.json') as f:
#                 sl = json.load(f)
#             if message[1] == 'send_weather':
#                 if message[2] == 'вкл':
#                     sl[peer_id]['can_send_weather'] = True
#                 elif message[2] == 'выкл':
#                     sl[peer_id]['can_send_weather'] = False
#                 else:
#                     send_message(peer_id, 'не правильный формат ввода')
#             elif message[1] == 'change_nik':
#                 if message[2] == 'вкл':
#                     sl[peer_id]['can_change_nik'] = True
#                 elif message[2] == 'выкл':
#                     sl[peer_id]['can_change_nik'] = False
#                 else:
#                     send_message(peer_id, 'не правильный формат ввода')
#             elif message[1] == 'send_random':
#                 if message[2] == 'вкл':
#                     sl[peer_id]['can_send_random'] = True
#                 elif message[2] == 'выкл':
#                     sl[peer_id]['can_send_random'] = False
#                 else:
#                     send_message(peer_id, 'не правильный формат ввода')
#             elif message[1] == 'add_new_subject':
#                 if message[2] in sl['subjects']:
#                     send_message(peer_id, 'этот предмет уже зарегистрирован')
#                     return 0
#                 sl[peer_id]['subjects'][message[2]] = []
#
#             else:
#                 send_message(peer_id, 'не правильный формат ввода')
#             with open('conversations.json', 'w') as f:
#                 f.write(json.dumps(sl, ensure_ascii=False))
#         except Exception:
#             send_message(peer_id,
#                          'Произошла ошибка, скорее всего'
#                          ' бот не администратор или не правильный формат ввода')
#     else:
#         send_message(peer_id, 'Не правильный формат смены настроек')


# def change_title(peer_id, message):
#     peer_id = str(peer_id)
#     message = message.split()
#     if message[0] != 'new_title:' or len(message) != 2:
#         send_message(peer_id, 'Не правильный формат ввода')
#         return 0
#     morph = pymorphy2.MorphAnalyzer()
#     word = morph.parse(message[1])[0]
#     if str(word.tag) == 'LATN':
#         send_message(peer_id, 'Введите титул на русском языке')
#         return 0
#     if str(word.tag) == 'UNKN':
#         send_message(peer_id, 'Введите титул без знаков препинания')
#         return 0
#     if str(word.tag.POS) != 'NOUN':
#         send_message(peer_id, 'Введённый титул должен быть существительным')
#         return 0
#     new_title = word.inflect({'ablt', 'sing'})
#     if new_title is None:
#         send_message(peer_id,
#                      'Произошла ошибка. Скорее всего это слово слишком редко случается.'
#                      ' Если вам действительно'
#                      ' надо поставить такой титул напишите @lambdafunction')
#         return 0
#     with open('conversations.json') as f:
#         sl = json.load(f)
#     sl[peer_id]['title'] = new_title.word
#     with open('conversations.json', 'w') as f:
#         f.write(json.dumps(sl, ensure_ascii=False))
#     send_message(peer_id,
#                  'Разыгрываемый титул изменён на "' + new_title.word +
#                  '". Если форма слова образована не правильно напишите @lambdafunction')


# def add_subject(peer_id, message):
#     peer_id = str(peer_id)
#     message = message.split()
#     if message[0] == 'add_subject' and len(message) == 2:
#         with open('conversations.json') as f:
#             sl = json.load(f)
#
#         sl[peer_id]['subjects'][message[1]] = []
#         with open('conversations.json', 'w') as f:
#             f.write(json.dumps(sl, ensure_ascii=False))
#     send_message(peer_id, 'Предмет добавлен')


# def transformation_date(peer_id, last_date):
#     if '.' not in last_date:
#         send_message(peer_id, 'Введите дату в формате DD.MM')
#         return 0
#     new_date = last_date.split('.')
#     mm = str(new_date[1])
#     dd = str(new_date[0])
#     if mm.isdigit() and dd.isdigit():
#         if int(mm) < 1 or int(mm) > 12:
#             send_message(peer_id, 'Колличество месяцев должено укладываться в рамки года')
#             return 0
#         if int(dd) < 1 or int(dd) > 31:
#             send_message(peer_id, 'Колличество дней должно укладываться в рамки месяца')
#             return 0
#         date = dd + '.' + mm
#         return date
#     send_message(peer_id, 'Дата и месяц длжны быть числами')
#     return 0


# def add_homework(peer_id, message, photos):
#     peer_id = str(peer_id)
#     message = message.split()
#     if message[0] != 'add_homework':
#         send_message(peer_id, 'Не правильный формат ввода')
#         return 0
#     if 'на' in message:
#         message.remove('на')
#     if len(message) < 4:
#         send_message(peer_id, 'Не правильный формат ввода')
#         return 0
#     lesson = message[1]
#     homework = ''
#     date = transformation_date(peer_id, message[2])
#     if date == 0:
#         return 0
#     for elem in message[3::]:
#         homework += elem + " "
#     with open('conversations.json') as f:
#         sl = json.load(f)
#     if lesson not in sl[peer_id]['subjects']:
#         send_message(peer_id, 'вы ввели не зарегистрированный предмет')
#         return 0
#     homework += '\nПрикреплённые фото: '
#     for elem in photos:
#         homework += elem
#         homework += ' '
#     sl[peer_id]['subjects'][lesson].append([date, homework])
#     with open('conversations.json', 'w') as f:
#         f.write(json.dumps(sl, ensure_ascii=False))
#     send_message(peer_id, "Успешно")


# def call_subject(peer_id, message):
#     message = message.split()
#     peer_id = str(peer_id)
#     if message[0] == 'дз' and len(message) >= 2:
#         if message[1] == 'по':
#             message.remove(message[1])
#             n = str(dt.datetime.now()).split(' ')[0].split('-')
#             now = int(n[1]) * 100 + int(n[2])
#             if message[-1] == 'все':
#                 message.remove('все')
#                 now = -1
#             if len(message) == 2:
#                 subject = message[1]
#                 with open('conversations.json') as f:
#                     sl = json.load(f)
#                 if subject in sl[peer_id]['subjects']:
#                     messag = ''
#                     for (date, homework) in sl[peer_id]['subjects'][subject]:
#                         d, m = map(int, date.split('.'))
#                         if now <= m * 100 + d:
#                             messag += ('Дз на ' + date + ':\n' + homework + '\n\n')
#                     send_message(peer_id, messag)
#         if message[1] == 'на':
#             data = message[2]
#             with open('conversations.json') as f:
#                 sl = json.load(f)
#                 messag = 'Дз на ' + data + '\n'
#                 for subject in sl[peer_id]['subjects']:
#                     for (date, homework) in sl[peer_id]['subjects'][subject]:
#                         if date == data:
#                             messag += 'Дз по ' + subject + '\n' + homework + '\n\n'
#             send_message(peer_id, messag)


def static_coronavirus(peer_id):
    url = 'https://api.thevirustracker.com/free-api?countryTotal=RU'
    response = requests.get(url).json()['countrydata'][0]
    message = 'Заражённых за весь период - {},\n' \
              'Заражённых на данный момент - {},\n' \
              'Заражённых за день - {},\n' \
              'Выздровевших за весь период - {},\n' \
              'Умерших за весь период - {},\n' \
              'Умерших за день - {}'.format(response['total_cases'], response['total_serious_cases'],
                                            response['total_new_cases_today'],
                                            response['total_recovered'],
                                            response['total_deaths'],
                                            response['total_new_deaths_today'])
    send_message(peer_id, message)


# def message_for_game(peer_id, message, from_id):
#     peer_id = str(peer_id)
#     from_id = str(from_id)
#     message = message.split()
#     if len(message) != 2 or message[0] != 'вызов':
#         return 0
#     message = message[1].split('|')
#     if message[0][0:3] != '[id':
#         return 0
#     id = message[0][3::]
#     with open('conversations.json') as f:
#         sl = json.load(f)
#     if sl[peer_id]['play_in_zeros'][id] == 1:
#         send_message(peer_id, 'Игроку уже брошен вызов')
#         return 0
#     if sl[peer_id]['play_in_zeros'][id] == 2:
#         send_message(peer_id, 'Игрок уже играет с кем-то')
#         return 0
#     if sl[peer_id]['play_in_zeros'][from_id] == 1:
#         send_message(peer_id, 'Вам уже брошен вызов')
#         return 0
#     if sl[peer_id]['play_in_zeros'][from_id] == 2:
#         send_message(peer_id, 'Вы уже играет с кем-то')
#         return 0
#     sl[peer_id]['play_in_zeros'][id] = 1
#     sl[peer_id]['play_in_zeros'][from_id] = 1
#     sl[peer_id]['waiting_for_confirmation'][id] = from_id
#     send_message(peer_id, '[id' + id + '|' + sl[peer_id]['names'][id] \
#                  + '] вам бросил вызов ' + '[id' + from_id + '|' + sl[peer_id]['names'][from_id] + ']')
#     with open('conversations.json', 'w') as f:
#         f.write(json.dumps(sl, ensure_ascii=False))


# def agree_game(peer_id, from_id):
#     peer_id = str(peer_id)
#     from_id = str(from_id)
#     with open('conversations.json') as f:
#         sl = json.load(f)
#     if from_id not in sl[peer_id]['waiting_for_confirmation']:
#         send_message(peer_id, 'Вам не поступало вызовов')
#         return 0
#     if sl[peer_id]['play_in_zeros'][from_id] != 1:
#         send_message(peer_id, 'Вам не поступало вызовов, либо вы уже играете с кем-то')
#         return 0
#     id = sl[peer_id]['waiting_for_confirmation'][from_id]
#     ids = sorted([id, from_id])
#     ids_for_sl = ids[0] + ids[1]
#     who_move = choice([0, 1])
#     sl[peer_id]['plaing_in_zeros'][id] = from_id
#     sl[peer_id]['plaing_in_zeros'][from_id] = id
#     sl[peer_id]['in_zeros'][ids_for_sl] = {}
#     field = ['1 ', ' 2 ', ' 3', '4 ', ' 5 ', ' 6', '7 ', ' 8 ', ' 9']
#     sl[peer_id]['in_zeros'][ids_for_sl]['field'] = field
#     sl[peer_id]['in_zeros'][ids_for_sl]['who_move'] = who_move
#     sl[peer_id]['in_zeros'][ids_for_sl]['first_player'] = ids[who_move]
#     sl[peer_id]['play_in_zeros'][id] = 2
#     sl[peer_id]['play_in_zeros'][from_id] = 2
#     send_message(peer_id, 'Первым ходит [id' + ids[who_move] + '|' + sl[peer_id]['names'][ids[who_move]] + ']')
#     send_message(peer_id, '{} | {} | {}\n'
#                           '---------------\n'
#                           '{} | {} | {}\n'
#                           '---------------\n'
#                           '{} | {} | {}'.format(field[0], field[1], field[2], field[3],
#                                                 field[4], field[5],
#                                                 field[6], field[7], field[8]))
#     with open('conversations.json', 'w') as f:
#         f.write(json.dumps(sl, ensure_ascii=False))


# def make_a_move(field, id, played):
#     if played == 1:
#         played = 'X'
#     else:
#         played = 'O'
#     if field[id] == "X" or field[id] == "O":
#         return field, 0
#     field[id] = played
#     a = [0, 0, 1, 2, 3, 6, 0, 2]
#     b = [1, 3, 4, 5, 4, 7, 4, 4]
#     c = [2, 6, 7, 8, 5, 8, 8, 6]
#     count = 0
#     for i in range(8):
#         if field[a[i]] == field[b[i]] == field[c[i]] != " ":
#             if field[a[i]] == 'X':
#                 field[a[i]] = '❌'
#                 field[b[i]] = '❌'
#                 field[c[i]] = '❌'
#                 return field, 1
#             elif field[a[i]] == 'O':
#                 field[a[i]] = '⭕'
#                 field[b[i]] = '⭕'
#                 field[c[i]] = '⭕'
#                 return field, 2
#     for i in range(9):
#         if field[i] == 'X' or field[i] == 'O':
#             count += 1
#     if count == 9:
#         return field, 4
#     return field, 3


# def zeros_playing(peer_id, from_id, message):
#     peer_id = str(peer_id)
#     from_id = str(from_id)
#     with open('conversations.json') as f:
#         sl = json.load(f)
#     message = message.split()
#     if len(message) != 2 or not message[1].isdigit():
#         return 0
#     if sl[peer_id]['play_in_zeros'][from_id] != 2:
#         send_message(peer_id, 'Вам не поступало вызовов, либо вы ещё не согласились')
#         return 0
#     if int(message[1]) < 1 or int(message[1]) > 9:
#         send_message(peer_id, 'Не правильные границы ввода')
#         return 0
#     user_id = sl[peer_id]['plaing_in_zeros'][from_id]
#     ids = sorted([from_id, user_id])
#     ids_for_sl = ids[0] + ids[1]
#     who_move = sl[peer_id]['in_zeros'][ids_for_sl]['who_move']
#     field = sl[peer_id]['in_zeros'][ids_for_sl]['field']
#     if ids[who_move] != from_id:
#         send_message(peer_id, 'Сейчас не ваша очередь ходить')
#         return 0
#     field, code = make_a_move(field, int(message[1]) - 1,
#                               sl[peer_id]['in_zeros'][ids_for_sl]['first_player'] == ids[who_move])
#     if code == 0:
#         send_message(peer_id, 'Эта клетка уже занята')
#         return 0
#     elif code == 4:
#         sl[peer_id]['play_in_zeros'][from_id] = 0
#         sl[peer_id]['play_in_zeros'][user_id] = 0
#         send_message(peer_id, 'Ничья')
#     elif code == 2:
#         sl[peer_id]['play_in_zeros'][from_id] = 0
#         sl[peer_id]['play_in_zeros'][user_id] = 0
#         if sl[peer_id]['in_zeros'][ids_for_sl]['first_player'] != from_id:
#             send_message(peer_id,
#                          'Выиграл [id' + ids[who_move] + '|' + sl[peer_id]['names'][ids[who_move]] + ']')
#         else:
#             send_message(peer_id,
#                          'Выиграл [id' + ids[1 - who_move] + '|' + sl[peer_id]['names'][ids[1 - who_move]] + ']')
#     elif code == 1:
#         sl[peer_id]['play_in_zeros'][from_id] = 0
#         sl[peer_id]['play_in_zeros'][user_id] = 0
#         if sl[peer_id]['in_zeros'][ids_for_sl]['first_player'] == from_id:
#             send_message(peer_id,
#                          'Выиграл [id' + ids[who_move] + '|' + sl[peer_id]['names'][ids[who_move]] + ']')
#         else:
#             send_message(peer_id,
#                          'Выиграл [id' + ids[1 - who_move] + '|' + sl[peer_id]['names'][ids[1 - who_move]] + ']')
#     elif code == 3:
#         send_message(peer_id, 'Продолжаем играть')
#     sl[peer_id]['in_zeros'][ids_for_sl]['who_move'] = 1 - who_move
#     send_message(peer_id, '{} | {} | {}\n'
#                           '------------\n'
#                           '{} | {} | {}\n'
#                           '------------\n'
#                           '{} | {} | {}'.format(field[0], field[1], field[2], field[3],
#                                                 field[4], field[5],
#                                                 field[6], field[7], field[8]))
#     with open('conversations.json', 'w') as f:
#         f.write(json.dumps(sl, ensure_ascii=False))


# def cancel_played(peer_id, from_id):
#     peer_id = str(peer_id)
#     from_id = str(from_id)
#     with open('conversations.json') as f:
#         sl = json.load(f)
#     sl[peer_id]['play_in_zeros'][from_id] = 0
#     if from_id in sl[peer_id]['play_in_zeros']:
#         sl[peer_id]['play_in_zeros'][sl[peer_id]['plaing_in_zeros'][from_id]] = 0
#     send_message(peer_id, 'Ok')
#     with open('conversations.json', 'w') as f:
#         f.write(json.dumps(sl, ensure_ascii=False))


def get_skin(nik):
    for i in range(1, 6):
        url = "https://ru.namemc.com/minecraft-skins/profile/" + nik + "." + str(i)
        res = requests.get(url)
        if '404 (Not Found)' in res:
            continue
        now_nik = res.text[res.text.find('<meta name="og:title" content="')::]
        now_nik = now_nik.split('"')[3].split()[0].lower()
        if now_nik == nik:
            text = res.text[res.text.find('<meta name="twitter:image" content="')::]
            text = text.split('"')[3].split('=')[1].split('&')[0]
            return text
    return 0


def message_for_skin(peer_id, message):
    message = message.split()
    code = get_skin(message[1])
    if code == 0:
        send_message(peer_id, 'Скорее всего игрока с таким ником не существует')
    else:
        send_message(peer_id, 'https://ru.namemc.com/skin/' + code)


# def get_text_wikipedia(i, message):
#     wikipedia.set_lang('uk')
#     r = wikipedia.search(message)
#     return wikipedia.page(r[i]).content
#
#
# def get_wikipedia(peer_id, message):
#     start_time = time.perf_counter()
#     for i in range(5):
#         try:
#             print(i)
#             text = get_text_wikipedia(i, message)
#             myobj = gTTS(text=text, lang='uk', slow=False)
#             myobj.save("voice1.mp3")
#             a = vk.docs.getMessagesUploadServer(type='audio_message', peer_id=peer_id)
#             print(1, a)
#             b = requests.post(a['upload_url'], files={
#                 'file': open("C:\\Users\\админ\\PycharmProjects\\asd\\vk_bot_for_school\\voice1.mp3",
#                              'rb')}).json()
#             print(2, b)
#             c = vk.docs.save(file=b["file"])['audio_message']
#             print(3, c)
#             d = 'audio{}_{}'.format(c['owner_id'], c['id'])
#             print(4, d)
#             print(text)
#             send_message(peer_id, text[:100:])
#             vk.messages.send(
#                 peer_id=peer_id,
#                 attachment=d,
#                 message='Здесь должна быть прикреплина аудиозапись с этой ссылкой ' + c['link_mp3'],
#                 random_id=randint(1, 100000000)
#             )
#             vk.messages.send(
#                 peer_id=peer_id,
#                 message='Запрос выполнялся ' + str(time.perf_counter() - start_time),
#                 random_id=randint(1, 100000000)
#             )
#             return 0
#         except Exception:
#             pass


# def random_char(peer_id, message):
#     num = str(message.split()[2])
#     if not num.isdigit():
#         return 0
#     num = int(num)
#     if num <= 0 or num > 501:
#         return 0
#     text = ''
#     for i in range(num):
#         text += chr(randint(1, 10000))
#     send_message(peer_id, text)


# def ismember(peer_id):
#     list_of_people = vk.messages.getConversationMembers(peer_id=peer_id)['profiles']
#     list_ids = []
#     for elem in list_of_people:
#         list_ids.append(elem['id'])
#     res = vk.groups.isMember(group_id=196697372, user_ids=list_ids)
#     with open('conversations.json') as f:
#         sl = json.load(f)
#     text = ''
#     for elem in res:
#         text += '[id' + str(elem['user_id']) + '|' + sl[str(peer_id)]['names'][str(elem['user_id'])] + '] - '
#         if elem['member']:
#             text += 'подписан\n'
#         else:
#             text += 'не подписан\n'
#     send_message(peer_id, text)


def game(from_id, peer_id, message):
    # проверяет значение переменной 'message', далее раскидывает по функциям
    # noinspection PyBroadException
    try:
        with open("game2.0.json") as g21:
            g = json.load(g21)
        # from_id = event.object['message']['from_id']
        # peer_id = event.object['message']['peer_id']
        # message = event.object['message']['text'].lower()
        print(1)
        if peer_id not in str(g):
            with open("game_copy.json") as g2121:
                g2 = json.load(g2121)
                g[peer_id] = g2
        with open("game2.0.json") as f:
            f.write(json.dumps(g, ensure_ascii=False))
        with open("game2.0.json") as g21:
            g = json.load(g21)
            if message == "правила 21":
                rules(peer_id, from_id)
            elif '21 с ' == message[:5] or '21 c ' == message[:5] and str(from_id) != message[8:17]:
                offer(g, from_id, message, peer_id)
            elif "[club196697372|@godofnatural] не хочу" == message and g[peer_id]["players"]["second"]["id"] \
                    == from_id and g[peer_id]["conversation"] == peer_id and g[peer_id]["request"]:
                not_offer(g, peer_id)
            elif "[club196697372|@godofnatural] принять" == message and g[peer_id]["players"]["second"]["id"] \
                    == from_id and g[peer_id]["conversation"] == peer_id and g[peer_id]["request"]:
                start_game(g, peer_id)
            elif "ещё карту" == message:
                more_carts(g, from_id)
            elif "достаточно!" == message:
                winner_game(g)
            elif "отмена 21" == message and g[peer_id]["game_now"] and (from_id == g[peer_id]["players"]["first"]["id"]
                                                               or from_id == g[peer_id]["players"]["second"][
                                                                   "id"] or from_id == 202073373):
                send_message(peer_id, "сделано")
                end(peer_id)
    except Exception:
        sleep(2)
        game(from_id, peer_id, message)


def rules(peer_id, from_id):
    # отправляет правила игры 21 в личные сообщения
    send_message(peer_id, "Выслал в личку")
    vk.messages.send(
        user_id=from_id,
        message="Бот сдает каждому игроку по две карты, все карты дают игроку определенное "
                "количество очков, туз - 11 очков, король - 4 очка, дама - 3 очка, валет - 2 очка, "
                "остальные карты по своему номиналу. Цель игрока - собрать 21 очко или наиболее "
                "близкое к нему число, после того, как игрок получил две карты, он может попросить "
                "еще, как уже было сказано, нужно собрать 21 или как можно ближе, но если собрать "
                "больше - это автоматическое поражение. Когда бот выдал игрокам столько карт, "
                "сколько они просили, игроки вскрываются и показывают карты, побеждает тот, "
                "кто собрал наиболее близкое количество очков к 21 или 21, но не больше.\n"
                'Для вызова пиши: "21 с @/.../"(пример "21 c @rollbollvlad"), '
                'чтобы принять, достаточно нажать на кнопку',
        random_id=randint(0, 1000000000),
    )


# def send_message(peer_id, message):  # отправка сообщения
#     peer_id = int(peer_id)
#     # noinspection PyBroadException
#     try:
#         vk.messages.send(
#             peer_id=peer_id,
#             message=message,
#             random_id=randint(0, 1000000000),
#         )
#     except Exception:
#         return 0


def offer(settings, from_id, message, peer_id):
    # отправляет предложение о игре в беседу, прилагая кнопки на сообщении
    if settings[peer_id]["game_now"]:
        send_message(peer_id,
                     'Подождите окончания игры! Или если вы являетесь участником, напишите "отмена 21"')
    else:
        user = vk.users.get(user_ids=from_id)
        settings[peer_id]["players"]["first"]["id"] = from_id
        settings[peer_id]["players"]["first"]["name"] = user[0]['first_name'] + ' ' + user[0]['last_name']
        user = vk.users.get(user_ids=message[8:17])
        settings[peer_id]["players"]["second"]["id"] = int(message[8:17])
        settings[peer_id]["players"]["second"]["name"] = user[0]['first_name'] + ' ' + user[0]['last_name']
        settings[peer_id]["request"] = True
        settings[peer_id]["conversation"] = peer_id
        keyboard = VkKeyboard(inline=True)
        keyboard.add_button("Принять", color=VkKeyboardColor.POSITIVE)
        keyboard.add_button("Не хочу", color=VkKeyboardColor.NEGATIVE)
        vk.messages.send(
            peer_id=settings[peer_id]["conversation"],
            message="Мы [" + message[6:17] + "|тебя] ждем",
            random_id=randint(0, 1000000000),
            keyboard=keyboard.get_keyboard(),
        )
        save(settings)


def send_message_user(user_id, message):
    # отправка сообщений ботом в личные сообщения, прилагая кнопки
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button("Ещё карту", color=VkKeyboardColor.NEGATIVE)
    keyboard.add_button("Достаточно!", color=VkKeyboardColor.POSITIVE)
    vk.messages.send(
        user_id=user_id,
        message=message,
        random_id=randint(0, 1000000000),
        keyboard=keyboard.get_keyboard(),
    )


def interaction(settings, from_id, peer_id):
    # выбирает рандомную карту, отправляет ее пользователю(в лс), удаляет ее из списка,
    # далее добавляет очки(за эту карту), выводит кол-во очков(ДЛЯ ПЕРВОГО ИГРОКА(ТОГО КТО ВЫЗЫВАЛ))
    cart = choice(settings[peer_id]["cards"])
    settings[peer_id]["cards"].remove(cart)
    if from_id == settings[peer_id]["players"]["first"]["id"]:
        settings[peer_id]["players"]["first"]["attempts"] += 1
        photo(settings[peer_id]["players"]["first"]["id"], "photo-197213529_4572390" + cart[0])
        settings[peer_id]['players']["first"]["score"] += cart[1]
        send_message_user(settings[peer_id]["players"]["first"]["id"],
                          "Ваши текущие очки - " + str(settings[peer_id]['players']["first"]["score"]))
    else:
        settings[peer_id]["players"]["second"]["attempts"] += 1
        photo(settings[peer_id]["players"]["second"]["id"], "photo-197213529_4572390" + cart[0])
        settings[peer_id]['players']["second"]["score"] += cart[1]
        send_message_user(settings[peer_id]["players"]["second"]["id"],
                          "Ваши текущие очки - " + str(settings[peer_id]['players']["second"]["score"]))
    save(settings)


def photo(user_id, photo_cart):
    # отправляет фото выбранное в функциях(players1/2)
    vk.messages.send(
        user_id=user_id,
        random_id=randint(0, 1000000000),
        attachment=photo_cart
    )


def end(peer_id):
    # резко завершает игру и обнуляет все в json файле
    with open("game_copy.json") as gg21:
        gg = json.load(gg21)
        with open('game2.0.json', 'w') as ggg:
            gggg = json.load(ggg)
            gggg[peer_id].write(json.dumps(gg, ensure_ascii=False))


def save(settings):
    # обязательное сохранение после почти каждой операции
    with open('game.json', 'w') as g21:
        g21.write(json.dumps(settings, ensure_ascii=False))


def winner_game(settings, peer_id):
    # выбирает победителя игры и заканчивает работу
    if not settings[peer_id]["checker_1"]:
        send_message(settings[peer_id]["conversation"], "Один игрок уже готов")
        settings[peer_id]["checker_1"] = True
        save(settings)
    else:
        if (settings[peer_id]["players"]["second"]["score"] < settings[peer_id]["players"]["first"]["score"] <= 21) \
                or (settings[peer_id]["players"]["second"]["score"] > 21 and settings[peer_id]["players"]["first"]["score"] <= 21):
            winner = "[id" + str(settings[peer_id]["players"]["first"]["id"])\
                     + "|" + settings[peer_id]["players"]["first"]["name"] + "]"
        elif (settings[peer_id]["players"]["first"]["score"] < settings[peer_id]["players"]["second"]["score"] <= 21) \
                or (settings[peer_id]["players"]["first"]["score"] > 21 and settings[peer_id]["players"]["second"]["score"] <= 21):
            winner = "[id" + str(settings[peer_id]["players"]["second"]["id"])\
                     + "|" + settings[peer_id]["players"]["second"]["name"] + "]"
        else:
            winner = "Увы, победителей нет("
        send_message(settings[peer_id]["conversation"], "Второй тоже, начинаем подводить итоги!")
        send_message(settings[peer_id]["conversation"],
                     "[id" + str(settings[peer_id]["players"]["first"]["id"]) + "|Инициатор] набрал " + str(
                         settings[peer_id]["players"]["first"]["score"]) +
                     " очков!\n" + "[id" + str(
                         settings[peer_id]["players"]["second"]["id"]) + "|Тот самый] получил " + str(
                         settings[peer_id]["players"]["second"]["score"]) +
                     " очков!\nПобедитель - " + winner)
        end(peer_id)


def more_carts(settings, from_id, peer_id):
    # проверка на абуз у человека, иначе переводит на функцию выдачи карты
    if settings[peer_id]["players"]["first"]["attempts"] > 10:
        send_message_user(settings[peer_id]["players"]["first"]["id"], "Как ты мог...")
        send_message_user(settings[peer_id]["players"]["second"]["id"],
                          "Первый игрок решил за-абузить бота, игра окончена")
        send_message(settings[peer_id]["conversation"],
                     "А, ну да, конечно, у нас завелся абузер, ник говорить не буду, "
                     "чтоб не хейтили")
        end(peer_id)
    elif settings[peer_id]["players"]["second"]["attempts"] > 10:
        send_message_user(settings[peer_id]["players"]["second"]["id"], "Как ты мог...")
        send_message_user(settings[peer_id]["players"]["first"]["id"],
                          "Второй игрок решил за-абузить бота, игра окончена")
        send_message(settings[peer_id]["conversation"],
                     "А, ну да, конечно, у нас завелся абузер, ник говорить не буду, "
                     "чтоб не хейтили")
        end(peer_id)
    else:
        interaction(settings, from_id, peer_id)


def start_game(settings, peer_id):
    # уродское начало игры
    send_message(settings[peer_id]["conversation"], "Игра начинается, чек лс")
    settings[peer_id]["game_now"] = True
    settings[peer_id]["request"] = False
    save(settings)
    send_message_user(settings[peer_id]["players"]["first"]["id"], "Ку бро, желаб удачи")
    send_message_user(settings[peer_id]["players"]["second"]["id"], "Тот чел внатуре езз, ты сможешь!")
    start_interaction(settings, peer_id)
    save(settings)


def not_offer(settings, peer_id):
    # отказ человека от игры
    send_message(settings[peer_id]["conversation"], "Ну и лан")
    settings[peer_id]["request"] = False
    end(peer_id)


def start_interaction(settings, peer_id):
    # уродская начальная выдача карт, фу
    for _ in range(2):
        cart = choice(settings[peer_id]["cards"])
        settings[peer_id]["cards"].remove(cart)
        photo(settings[peer_id]["players"]["first"]["id"], "photo-197213529_4572390" + cart[0])
        settings[peer_id]['players']["first"]["score"] += cart[1]
        send_message_user(settings[peer_id]["players"]["first"]["id"],
                          "Ваши текущие очки - " + str(settings[peer_id]['players']["first"]["score"]))
        save(settings)
        cart = choice(settings[peer_id]["cards"])
        settings[peer_id]["cards"].remove(cart)
        photo(settings[peer_id]["players"]["second"]["id"], "photo-197213529_4572390" + cart[0])
        settings[peer_id]['players']["second"]["score"] += cart[1]
        send_message_user(settings[peer_id]["players"]["second"]["id"],
                          "Ваши текущие очки - " + str(settings[peer_id]['players']["second"]["score"]))
        save(settings)


token = "ffe517a0e394b9d6df6d624d16dd58102ad0de99c8c8f08468628085d7e11e5d08953b42d69e553fccc64"
api_key = '52d406bba24fd0df794d9978adcfc392'
ur = 'https://api.openweathermap.org/data/2.5/onecall?lat=57.656520&lon=39.835397&lang=ru&exclude' \
     '=current&appid=' + api_key
vkBotSession = VkApi(token=token)
groupId = 196697372
VkBotLongPoll = VkBotLongPoll(vkBotSession, groupId)
vk = vkBotSession.get_api()
