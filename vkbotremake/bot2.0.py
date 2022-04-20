import json
from random import randint, choice
import pymorphy2
import wikipedia
from gtts import gTTS
# from pprint import pprint
import requests
from vk_api import VkApi
import datetime as dt
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
import time


class Bot:
    def __init__(self, peer_id, message, from_id, photos):
        self.peer_id = peer_id
        self.message = message
        self.from_id = from_id
        self.photos = photos
        self.new()
        self.check_people()
        self.check_message()

    def check_message(self):
        if self.message[0:17:] == 'рандомный символ ':
            self.random_char()
        elif self.message == 'подписаны ли на группу' or self.message == "лень писат":
            self.ismember()
        elif self.message == 'команды':
            self.send_message('Команды бота доступны по ссылке:\nvk.com/@godofnatural-komandy-bota')
        elif self.message == 'рандом':
            self.random_user()
        elif self.message == 'статистика':
            self.get_static()
        elif '+ник' in self.message:
            self.change_nik_from()
        elif 'new_title:' in self.message:
            self.change_title()
        elif '+setting ' in self.message:
            self.change_settings()
        elif self.message == 'создатель' or self.message == 'создатели' or self.message \
                == 'создатель этого бота' or self.message == 'создатель бота' or \
                'создатели этого бота' in self.message or 'создатели этого бота' in self.message:
            self.send_message('Создатели этого прекрасного (нет) бота:\n'
                              '[id202073373|Владислав Селезнёв],\n'
                              '[id136611246|Чистяков Александр]\n'
                              'Вопросы, пожелания и баги посылать [id136611246|'
                              'ему]\n'
                              'Бот хостится на pythonanywhere.com, хостинг очень'
                              ' слабый и если вы хотите помочь,'
                              ' то напишите [id136611246|'
                              'ему]')
        elif 'add_homework' in self.message:
            self.add_homework()
        elif 'игра ' == self.message[0:5]:
            self.zeros_playing()
        elif 'вызов' in self.message:
            self.message_for_game()
        elif 'принять' == self.message or self.message == '@godofnatural принять':
            self.agree_game()
        elif self.message == 'игра отмена':
            self.cancel_played()
        elif 'погода на' in self.message or self.message == 'погода':
            self.get_weather()
        elif '+setting ' in self.message:
            self.change_settings()
        elif 'add_subject' in self.message:
            self.add_subject()
        elif 'дз ' == self.message[0:3]:
            self.call_subject()
        elif self.message[0:10:] == 'википедия ':
            self.send_message("Ищу " + self.message[10:])
            self.get_wikipedia()
        elif self.message[0:4] == 'бан ':
            self.delete_user()
        elif "мут " in self.message:
            self.send_message("я тебя щас забаню нахуй еблан")

    def send_message(self, message):  # отправка сообщения
        self.peer_id = int(self.peer_id)
        vk.messages.send(
            peer_id=self.peer_id,
            message=message,
            random_id=randint(0, 1000000000),
        )

    def random_char(self):
        num = str(self.message.split()[2])
        if not num.isdigit():
            return 0
        num = int(num)
        if num <= 0 or num > 501:
            return 0
        text = ''
        for i in range(num):
            text += chr(randint(1, 10000))
        self.send_message(text)

    def new(self):  # проверка беседы
        self.peer_id = str(self.peer_id)
        with open('list_of_conversations.json') as f:
            sp = json.load(f)
        if self.peer_id in sp:  # если такая беседа уже была, то ничего не делается
            return 0
        sp.append(self.peer_id)  # если этой беседы ещё не было, то создаётся json файл со словарём
        with open('list_of_conversations.json', 'w') as f:
            f.write(json.dumps(sp, ensure_ascii=False))
        sl = {'names': {}, 'can_send_weather': True, 'can_send_random': True,
              'can_change_nik': True, 'static_for_random': {}, 'list_id': [], 'title': 'натуралом', 'subjects': {},
              'play_in_zeros': {}, 'waiting_for_confirmation': {}, 'plaing_in_zeros': {}, 'in_zeros': {}}
        try:
            list_of_people = vk.messages.getConversationMembers(peer_id=self.peer_id)
            for people in list_of_people['profiles']:
                sl['list_id'].append(str(people['id']))
                sl['names'][str(people['id'])] = people['first_name'] + " " + people['last_name']
                sl['play_in_zeros'][str(people['id'])] = 0
                sl['static_for_random'][str(people['id'])] = 0
            with open('conversations.json') as f:
                sp228 = json.load(f)
            sp228[self.peer_id] = sl
            with open('conversations.json', 'w') as f:
                f.write(json.dumps(sp228, ensure_ascii=False))
        except Exception:
            self.send_message('Пожалуйста, сделайте бота админом')

    def change_nik(self, user_id, new_name):  # смена ника
        self.peer_id = str(self.peer_id)
        user_id = str(user_id)
        with open('conversations.json') as f:
            sl = json.load(f)
        if not sl[self.peer_id]['can_change_nik']:
            self.send_message('Смена ника в беседе запрещена')
        sl[self.peer_id]['names'][user_id] = new_name
        self.send_message('Ok')
        with open('conversations.json', 'w') as f:
            f.write(json.dumps(sl, ensure_ascii=False))

    def check_people(self):  # проверка был ли человек в это беседе и раньше
        peer_id = str(self.peer_id)  # надо переделать, чтобы вызывалась только при определённом event
        user_id = str(self.from_id)
        with open('conversations.json') as f:
            sl = json.load(f)
        new_sl = {}
        if user_id not in sl[peer_id]['list_id']:
            sl[peer_id]['list_id'].append(user_id)
            list_of_people = vk.messages.getConversationMembers(peer_id=peer_id)
            for people in list_of_people['profiles']:
                if str(people['id']) in sl[peer_id]['names']:
                    new_sl[str(people['id'])] = sl[peer_id]['names'][str(people['id'])]
                else:
                    new_sl[str(people['id'])] = people['first_name'] + " " + people['last_name']
                    sl[peer_id]['static_for_random'][str(people['id'])] = 0
                    sl[peer_id]['list_id'].append(str(people['id']))
                    sl[peer_id]['play_in_zeros'][str(people['id'])] = 0
            sl[peer_id]['names'] = new_sl
        with open('conversations.json', 'w') as f:
            f.write(json.dumps(sl, ensure_ascii=False))

    def random_user(self):  # функция для рандомного выбора
        peer_id = str(self.peer_id)
        with open('conversations.json') as f:
            sl = json.load(f)
        if sl[peer_id]['can_send_random']:
            random_id = str(choice(sl[peer_id]['list_id']))
            sl[peer_id]['static_for_random'][random_id] += 1
            self.send_message('Сегодня ' + sl[peer_id]['title'] + ' становится: [id' + random_id + '|' +
                              sl[peer_id]['names'][random_id] + ']')
        else:
            self.send_message('Команда в этой беседе запрещена')
        with open('conversations.json', 'w') as f:
            f.write(json.dumps(sl, ensure_ascii=False))

    def get_static(self):  # функция для выдачи статистики
        peer_id = str(self.peer_id)
        with open('conversations.json') as f:
            sl = json.load(f)
        message = ''
        for user_id in sl[peer_id]['static_for_random']:
            message += '[id' + user_id + '|' + sl[peer_id]['names'][user_id] + ']: ' + str(
                sl[peer_id]['static_for_random'][user_id]) + '\n'
        self.send_message(message)

    def change_nik_from(self):  # функция по смене ника
        peer_id = str(self.peer_id)
        with open('conversations.json') as f:
            sl = json.load(f)
        if not sl[peer_id]['can_change_nik']:
            self.send_message('Команда запрещена в этой беседе')
        elif len(self.message) > 54:
            self.send_message('Ограничение по длине - 50 символов')
        elif self.message[0:5] != '+ник ':
            return 0
        else:
            self.change_nik(self.from_id, self.message[5::])

    def ismember(self):
        list_of_people = vk.messages.getConversationMembers(peer_id=self.peer_id)['profiles']
        list_ids = []
        for elem in list_of_people:
            list_ids.append(elem['id'])
        res = vk.groups.isMember(group_id=196697372, user_ids=list_ids)
        with open('conversations.json') as f:
            sl = json.load(f)
        text = ''
        for elem in res:
            text += '[id' + str(elem['user_id']) + '|' + sl[str(self.peer_id)]['names'][str(elem['user_id'])] + '] - '
            if elem['member']:
                text += 'подписан\n'
            else:
                text += 'не подписан\n'
        self.send_message(text)

    def change_settings(self):  # обрабатывает изменение настроек
        peer_id = str(self.peer_id)
        message = self.message.split()
        if message[0] == '+setting' and len(message) > 2:
            print(message)
            try:
                with open('conversations.json') as f:
                    sl = json.load(f)
                if message[1] == 'send_weather':
                    if message[2] == 'вкл':
                        sl[peer_id]['can_send_weather'] = True
                    elif message[2] == 'выкл':
                        sl[peer_id]['can_send_weather'] = False
                    else:
                        self.send_message('не правильный формат ввода')
                elif message[1] == 'change_nik':
                    if message[2] == 'вкл':
                        sl[peer_id]['can_change_nik'] = True
                    elif message[2] == 'выкл':
                        sl[peer_id]['can_change_nik'] = False
                    else:
                        self.send_message('не правильный формат ввода')
                elif message[1] == 'send_random':
                    if message[2] == 'вкл':
                        sl[peer_id]['can_send_random'] = True
                    elif message[2] == 'выкл':
                        sl[peer_id]['can_send_random'] = False
                    else:
                        self.send_message('не правильный формат ввода')
                elif message[1] == 'add_new_subject':
                    if message[2] in sl['subjects']:
                        self.send_message('этот предмет уже зарегистрирован')
                        return 0
                    sl[peer_id]['subjects'][message[2]] = []

                else:
                    self.send_message('не правильный формат ввода')
                with open('conversations.json', 'w') as f:
                    f.write(json.dumps(sl, ensure_ascii=False))
            except Exception:
                self.send_message('Произошла ошибка, скорее всего'
                                  ' бот не администратор или не правильный формат ввода')
        else:
            self.send_message('Не правильный формат смены настроек')

    def change_title(self):
        peer_id = str(self.peer_id)
        message = self.message.split()
        if message[0] != 'new_title:' or len(message) != 2:
            self.send_message('Не правильный формат ввода')
            return 0
        morph = pymorphy2.MorphAnalyzer()
        word = morph.parse(message[1])[0]
        if str(word.tag) == 'LATN':
            self.send_message('Введите титул на русском языке')
            return 0
        if str(word.tag) == 'UNKN':
            self.send_message('Введите титул без знаков препинания')
            return 0
        if str(word.tag.POS) != 'NOUN':
            self.send_message('Введённый титул должен быть существительным')
            return 0
        new_title = word.inflect({'ablt', 'sing'})
        if new_title is None:
            self.send_message('Произошла ошибка. Скорее всего это слово слишком редко случается.'
                              ' Если вам действительно'
                              ' надо поставить такой титул напишите @lambdafunction')
            return 0
        with open('conversations.json') as f:
            sl = json.load(f)
        sl[peer_id]['title'] = new_title.word
        with open('conversations.json', 'w') as f:
            f.write(json.dumps(sl, ensure_ascii=False))
        self.send_message('Разыгрываемый титул изменён на "' + new_title.word +
                          '". Если форма слова образована не правильно напишите @lambdafunction')

    def add_subject(self):
        peer_id = str(self.peer_id)
        message = self.message.split()
        if message[0] == 'add_subject' and len(message) == 2:
            with open('conversations.json') as f:
                sl = json.load(f)

            sl[peer_id]['subjects'][message[1]] = []
            with open('conversations.json', 'w') as f:
                f.write(json.dumps(sl, ensure_ascii=False))
        self.send_message('Предмет добавлен')

    def transformation_date(self, last_date):
        if '.' not in last_date:
            self.send_message('Введите дату в формате DD.MM')
            return 0
        new_date = last_date.split('.')
        mm = str(new_date[1])
        dd = str(new_date[0])
        if mm.isdigit() and dd.isdigit():
            if int(mm) < 1 or int(mm) > 12:
                self.send_message('Колличество месяцев должено укладываться в рамки года')
                return 0
            if int(dd) < 1 or int(dd) > 31:
                self.send_message('Колличество дней должно укладываться в рамки месяца')
                return 0
            date = dd + '.' + mm
            return date
        self.send_message('Дата и месяц длжны быть числами')
        return 0

    def add_homework(self):
        peer_id = str(self.peer_id)
        message = self.message.split()
        if message[0] != 'add_homework':
            self.send_message('Не правильный формат ввода')
            return 0
        if 'на' in message:
            message.remove('на')
        if len(message) < 4:
            self.send_message('Не правильный формат ввода')
            return 0
        lesson = message[1]
        homework = ''
        date = self.transformation_date(message[2])
        if date == 0:
            return 0
        for elem in message[3::]:
            homework += elem + " "
        with open('conversations.json') as f:
            sl = json.load(f)
        if lesson not in sl[peer_id]['subjects']:
            self.send_message('вы ввели не зарегистрированный предмет')
            return 0
        homework += '\nПрикреплённые фото: '
        for elem in self.photos:
            homework += elem
            homework += ' '
        sl[peer_id]['subjects'][lesson].append([date, homework])
        with open('conversations.json', 'w') as f:
            f.write(json.dumps(sl, ensure_ascii=False))
        self.send_message("Успешно")

    def call_subject(self):
        message = self.message.split()
        peer_id = str(self.peer_id)
        if message[0] == 'дз' and len(message) >= 2:
            if message[1] == 'по':
                message.remove(message[1])
                n = str(dt.datetime.now()).split(' ')[0].split('-')
                now = int(n[1]) * 100 + int(n[2])
                if message[-1] == 'все':
                    message.remove('все')
                    now = -1
                if len(message) == 2:
                    subject = message[1]
                    with open('conversations.json') as f:
                        sl = json.load(f)
                    if subject in sl[peer_id]['subjects']:
                        message_ = ''
                        for (date, homework) in sl[peer_id]['subjects'][subject]:
                            d, m = map(int, date.split('.'))
                            if now <= m * 100 + d:
                                message_ += ('Дз на ' + date + ':\n' + homework + '\n\n')
                        self.send_message(message_)
            if message[1] == 'на':
                data = message[2]
                with open('conversations.json') as f:
                    sl = json.load(f)
                    message_ = 'Дз на ' + data + '\n'
                    for subject in sl[peer_id]['subjects']:
                        for (date, homework) in sl[peer_id]['subjects'][subject]:
                            if date == data:
                                message_ += 'Дз по ' + subject + '\n' + homework + '\n\n'
                self.send_message(message_)

    def message_for_game(self):
        peer_id = str(self.peer_id)
        from_id = str(self.from_id)
        message = self.message.split()
        if len(message) != 2 or message[0] != 'вызов':
            return 0
        message = message[1].split('|')
        if message[0][0:3] != '[id':
            return 0
        id = message[0][3::]
        with open('conversations.json') as f:
            sl = json.load(f)
        if sl[peer_id]['play_in_zeros'][id] == 1:
            self.send_message('Игроку уже брошен вызов')
            return 0
        if sl[peer_id]['play_in_zeros'][id] == 2:
            self.send_message('Игрок уже играет с кем-то')
            return 0
        if sl[peer_id]['play_in_zeros'][from_id] == 1:
            self.send_message('Вам уже брошен вызов')
            return 0
        if sl[peer_id]['play_in_zeros'][from_id] == 2:
            self.send_message('Вы уже играет с кем-то')
            return 0
        sl[peer_id]['play_in_zeros'][id] = 1
        sl[peer_id]['play_in_zeros'][from_id] = 1
        sl[peer_id]['waiting_for_confirmation'][id] = from_id
        self.send_message('[id' + id + '|' + sl[peer_id]['names'][id]
                          + '] вам бросил вызов ' + '[id' + from_id + '|' + sl[peer_id]['names'][from_id] + ']')
        with open('conversations.json', 'w') as f:
            f.write(json.dumps(sl, ensure_ascii=False))

    def agree_game(self):
        peer_id = str(self.peer_id)
        from_id = str(self.from_id)
        with open('conversations.json') as f:
            sl = json.load(f)
        if from_id not in sl[peer_id]['waiting_for_confirmation']:
            self.send_message('Вам не поступало вызовов')
            return 0
        if sl[peer_id]['play_in_zeros'][from_id] != 1:
            self.send_message('Вам не поступало вызовов, либо вы уже играете с кем-то')
            return 0
        id = sl[peer_id]['waiting_for_confirmation'][from_id]
        ids = sorted([id, from_id])
        ids_for_sl = ids[0] + ids[1]
        who_move = choice([0, 1])
        sl[peer_id]['plaing_in_zeros'][id] = from_id
        sl[peer_id]['plaing_in_zeros'][from_id] = id
        sl[peer_id]['in_zeros'][ids_for_sl] = {}
        field = ['1 ', ' 2 ', ' 3', '4 ', ' 5 ', ' 6', '7 ', ' 8 ', ' 9']
        sl[peer_id]['in_zeros'][ids_for_sl]['field'] = field
        sl[peer_id]['in_zeros'][ids_for_sl]['who_move'] = who_move
        sl[peer_id]['in_zeros'][ids_for_sl]['first_player'] = ids[who_move]
        sl[peer_id]['play_in_zeros'][id] = 2
        sl[peer_id]['play_in_zeros'][from_id] = 2
        self.send_message('Первым ходит [id' + ids[who_move] + '|' + sl[peer_id]['names'][ids[who_move]] + ']')
        self.send_message('{} | {} | {}\n'
                          '---------------\n'
                          '{} | {} | {}\n'
                          '---------------\n'
                          '{} | {} | {}'.format(field[0], field[1], field[2], field[3],
                                                field[4], field[5],
                                                field[6], field[7], field[8]))
        with open('conversations.json', 'w') as f:
            f.write(json.dumps(sl, ensure_ascii=False))

    def zeros_playing(self):
        peer_id = str(self.peer_id)
        from_id = str(self.from_id)

        def make_a_move(field, id, played):
            if played == 1:
                played = 'X'
            else:
                played = 'O'
            if field[id] == "X" or field[id] == "O":
                return field, 0
            field[id] = played
            a = [0, 0, 1, 2, 3, 6, 0, 2]
            b = [1, 3, 4, 5, 4, 7, 4, 4]
            c = [2, 6, 7, 8, 5, 8, 8, 6]
            count = 0
            for i in range(8):
                if field[a[i]] == field[b[i]] == field[c[i]] != " ":
                    if field[a[i]] == 'X':
                        field[a[i]] = '❌'
                        field[b[i]] = '❌'
                        field[c[i]] = '❌'
                        return field, 1
                    elif field[a[i]] == 'O':
                        field[a[i]] = '⭕'
                        field[b[i]] = '⭕'
                        field[c[i]] = '⭕'
                        return field, 2
            for i in range(9):
                if field[i] == 'X' or field[i] == 'O':
                    count += 1
            if count == 9:
                return field, 4
            return field, 3

        with open('conversations.json') as f:
            sl = json.load(f)
        message = self.message.split()
        if len(message) != 2 or not message[1].isdigit():
            return 0
        if sl[peer_id]['play_in_zeros'][from_id] != 2:
            self.send_message('Вам не поступало вызовов, либо вы ещё не согласились')
            return 0
        if int(message[1]) < 1 or int(message[1]) > 9:
            self.send_message('Не правильные границы ввода')
            return 0
        user_id = sl[peer_id]['plaing_in_zeros'][from_id]
        ids = sorted([from_id, user_id])
        ids_for_sl = ids[0] + ids[1]
        who_move = sl[peer_id]['in_zeros'][ids_for_sl]['who_move']
        field = sl[peer_id]['in_zeros'][ids_for_sl]['field']
        if ids[who_move] != from_id:
            self.send_message('Сейчас не ваша очередь ходить')
            return 0
        field, code = make_a_move(field, int(message[1]) - 1,
                                  sl[peer_id]['in_zeros'][ids_for_sl]['first_player'] == ids[who_move])
        if code == 0:
            self.send_message('Эта клетка уже занята')
            return 0
        elif code == 4:
            sl[peer_id]['play_in_zeros'][from_id] = 0
            sl[peer_id]['play_in_zeros'][user_id] = 0
            self.send_message('Ничья')
        elif code == 2:
            sl[peer_id]['play_in_zeros'][from_id] = 0
            sl[peer_id]['play_in_zeros'][user_id] = 0
            if sl[peer_id]['in_zeros'][ids_for_sl]['first_player'] != from_id:
                self.send_message('Выиграл [id' + ids[who_move] + '|' + sl[peer_id]['names'][ids[who_move]] + ']')
            else:
                self.send_message(
                    'Выиграл [id' + ids[1 - who_move] + '|' + sl[peer_id]['names'][ids[1 - who_move]] + ']')
        elif code == 1:
            sl[peer_id]['play_in_zeros'][from_id] = 0
            sl[peer_id]['play_in_zeros'][user_id] = 0
            if sl[peer_id]['in_zeros'][ids_for_sl]['first_player'] == from_id:
                self.send_message('Выиграл [id' + ids[who_move] + '|' + sl[peer_id]['names'][ids[who_move]] + ']')
            else:
                self.send_message(
                    'Выиграл [id' + ids[1 - who_move] + '|' + sl[peer_id]['names'][ids[1 - who_move]] + ']')
        elif code == 3:
            self.send_message('Продолжаем играть')
        sl[peer_id]['in_zeros'][ids_for_sl]['who_move'] = 1 - who_move
        self.send_message('{} | {} | {}\n'
                          '------------\n'
                          '{} | {} | {}\n'
                          '------------\n'
                          '{} | {} | {}'.format(field[0], field[1], field[2], field[3],
                                                field[4], field[5],
                                                field[6], field[7], field[8]))
        with open('conversations.json', 'w') as f:
            f.write(json.dumps(sl, ensure_ascii=False))

    def cancel_played(self):
        peer_id = str(self.peer_id)
        from_id = str(self.from_id)
        with open('conversations.json') as f:
            sl = json.load(f)
        sl[peer_id]['play_in_zeros'][from_id] = 0
        if from_id in sl[peer_id]['play_in_zeros']:
            sl[peer_id]['play_in_zeros'][sl[peer_id]['plaing_in_zeros'][from_id]] = 0
        self.send_message('Ok')
        with open('conversations.json', 'w') as f:
            f.write(json.dumps(sl, ensure_ascii=False))

    def from_second_to_date(self, ts):  # перевод из секунд в дату
        return dt.datetime.utcfromtimestamp(ts)

    def get_weather(self):  # эта функция обрабатывает сообщение с погодой и вызывает различные функции
        peer_id = str(self.peer_id)
        message = self.message
        with open('conversations.json') as f:
            sl = json.load(f)
        if not sl[peer_id]['can_send_weather']:
            self.send_message('Команда в этой беседе запрещена')
            return 0
        if message == 'погода' or message == 'Погода на сегодня':
            self.get_weather_to_some_days(1)
            return 0
        elif message == 'погода на завтра' or message == 'погода на завтро':
            self.get_weather_to_tomorrow()
            return 0
        message = message.split()
        if len(message) > 2:
            if message[2].isdigit():
                num = int(message[2])
                if num > 8:
                    self.send_message('Слишком большое количество дней')
                elif num < 1:
                    self.send_message('Слишком маленькое количество дней')
                else:
                    self.get_weather_to_some_days(num)
            else:
                self.send_message('Не правильный формат ввода')
        else:
            self.send_message('Ошибка')

    def get_weather_to_tomorrow(self):  # возращает сообщение с погодой на завтра
        weather = self.get_weather_days(2)
        i = 1
        date = str(self.from_second_to_date(weather[str(i) + 'date']))[:-8]
        message_ = ''
        message_ += 'Погода на {}\n\n' \
                    'Днём {}°, ощущается как {}°\n' \
                    'Ночью {}°, ощущается как {}°\n' \
                    'Будет {}\n' \
                    'Ветер {} М/С\n\n\n'.format(date,
                                                weather[
                                                    str(i) + 'temp_afternoon'],
                                                weather[str(
                                                    i) + 'feels_temp_afternoon'],
                                                weather[str(i) + 'temp_night'],
                                                weather[str(
                                                    i) + 'feels_temp_night'],
                                                weather[str(i) + 'clouds'],
                                                weather[str(i) + 'wind_speed'])
        self.send_message(message_)

    def get_weather_to_some_days(self,
                                 num):  # возращает сообщение с погодой на определённое число дней
        messag = ''
        weather = self.get_weather_days(num)
        for i in range(num):
            date = str(self.from_second_to_date(weather[str(i) + 'date']))[:-8]
            messag += 'Погода на {}\n\n' \
                      'Днём {}°, ощущается как {}°\n' \
                      'Ночью {}°, ощущается как {}°\n' \
                      'Будет {}\n' \
                      'Ветер {} М/С\n\n\n'.format(date,
                                                  weather[
                                                      str(i) + 'temp_afternoon'],
                                                  weather[str(
                                                      i) + 'feels_temp_afternoon'],
                                                  weather[str(i) + 'temp_night'],
                                                  weather[str(
                                                      i) + 'feels_temp_night'],
                                                  weather[str(i) + 'clouds'],
                                                  weather[str(i) + 'wind_speed'])
        self.send_message(messag)

    def get_weather_days(self, num):  # отправляет API запрос для погоды и преобразует его в удобную форму
        api_key = '52d406bba24fd0df794d9978adcfc392'
        url = 'https://api.openweathermap.org/data/2.5/onecall?lat=57.656520&lon=39.835397&lang=ru&exclude' \
              '=current&appid=' + api_key
        response = requests.get(url)
        weather = response.json()
        res_weather = {}
        for n in range(num):
            res_weather[str(n) + 'temp_evening'] = int(weather['daily'][n]['temp']['eve'] - 273.15)
            res_weather[str(n) + 'temp_morning'] = int(weather['daily'][n]['temp']['morn'] - 273.15)
            res_weather[str(n) + 'temp_night'] = int(weather['daily'][n]['temp']['night'] - 273.15)
            res_weather[str(n) + 'temp_afternoon'] = int(weather['daily'][n]['temp']['day'] - 273.15)
            res_weather[str(n) + 'feels_temp_evening'] = int(
                weather['daily'][n]['feels_like']['eve'] - 273.15)
            res_weather[str(n) + 'feels_temp_morning'] = int(
                weather['daily'][n]['feels_like']['morn'] - 273.15)
            res_weather[str(n) + 'feels_temp_night'] = int(
                weather['daily'][n]['feels_like']['night'] - 273.15)
            res_weather[str(n) + 'feels_temp_afternoon'] = int(
                weather['daily'][n]['feels_like']['day'] - 273.15)
            res_weather[str(n) + 'wind_speed'] = int(weather['daily'][n]['wind_speed'])
            res_weather[str(n) + 'date'] = int(weather['daily'][n]['dt'])
            res_weather[str(n) + 'id'] = weather['daily'][0]['weather'][0]['icon']
            res_weather[str(n) + 'clouds'] = weather['daily'][n]['weather'][0]['description']
        return res_weather

    def get_wikipedia(self):
        start_time = time.perf_counter()
        peer_id = self.peer_id
        message = self.message[10::]

        def get_text_wikipedia(message):
            wikipedia.set_lang('ru')
            r = wikipedia.search(message)
            return wikipedia.page(r[0]).content

        try:
            text = get_text_wikipedia(message).split("\n")[0]
            # text = text.split("\n")[0]
            # print(imgs)
            myobj = gTTS(text=text, lang='ru', slow=True)
            myobj.save("voice1.mp3")
            a = vk.docs.getMessagesUploadServer(type='audio_message', peer_id=peer_id)
            b = requests.post(a['upload_url'], files={
                'file': open("D:\\python\\vkbotremake\\voice1.mp3",
                             'rb')}).json()
            a2 = vk.method("photos.getMessagesUploadServer")
            f = requests.post(a2['upload_url'], files={'photo': open('res.jpg', 'rb')}).json()
            cc = vk.method('photos.saveMessagesPhoto', {'photo': f['photo'], 'server': f['server'], 'hash': f['hash']})[
                0]
            dd = "photo{}_{}".format(cc["owner_id"], cc["id"])
            vk.messages.send(
                peer_id=peer_id,
                attachment=dd,
                message='бебра',
                random_id=randint(1, 100000000)
            )
            #vk.method("messages.send", {"peer_id": s, "message": "Ваша картинка", "attachment": d, "random_id": 0})
            c = vk.docs.save(file=b["file"])['audio_message']
            d = 'audio{}_{}'.format(c['owner_id'], c['id'])
            self.send_message(text)
            vk.messages.send(
                peer_id=peer_id,
                attachment=d,
                message='Здесь должна быть прикреплина аудиозапись с этой ссылкой ' + c['link_mp3'],
                random_id=randint(1, 100000000)
            )
            vk.messages.send(
                peer_id=peer_id,
                message='Запрос выполнялся ' + str
                (time.perf_counter() - start_time),
                random_id=randint(1, 100000000)
            )
            return 0
        except Exception:
            pass


def main():
    while True:
        for event in VkBotLongPoll.listen():
            if 'message' not in event.object:
                continue
            peer_id = event.object['message']['peer_id']
            message = (event.object['message']['text']).lower() if (
                event.object['message']['text']).lower() else " "
            from_id = event.object['message']['from_id']
            photos = [elem['photo']['sizes'][-1]['url'] for elem in event.object['message']['attachments']
                      if elem['type'] == 'photo']
            Bot(peer_id, message, from_id, photos)

            # elif message == "правила 21" or message.split()[0] == "21" \
            #         or message == "[club196697372|@godofnatural] не хочу" \
            #         or message == "[club196697372|@godofnatural] принять" or message == "ещё карту" \
            #         or message == "достаточно!" or message == "отмена 21":
            #     game(from_id, peer_id, message)
            # elif message == 'коронавирус статистика' or message == 'статистика коронавирус' \
            #         or message == 'стата коронавирус' or message == 'коронавирус стата':
            #     static_coronavirus(peer_id)
            # elif message[0:6] == '!скин ':
            #     message_for_skin(peer_id, message)


token = "ffe517a0e394b9d6df6d624d16dd58102ad0de99c8c8f08468628085d7e11e5d08953b42d69e553fccc64"
vkBotSession = VkApi(token=token)
groupId = 196697372
VkBotLongPoll = VkBotLongPoll(vkBotSession, groupId)
vk = vkBotSession.get_api()
main()
