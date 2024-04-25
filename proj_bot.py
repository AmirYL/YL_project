import telebot
from bot_token import YLP_TOKEN
from copy import deepcopy
import random
import requests
import datetime
import threading

bot = telebot.TeleBot(YLP_TOKEN)

sad_words = ["одиноко", "грустно",
             "невесело", "печально"]
sad_caption = ['Знаешь, мне кажется, что тебе грустно, потому что ты осознанно или нет отстранился от',
               'своих близких людей. Помни, что у тебя всегда будут те, кто может прийти на помощь']
help_message = ['Всё-таки нужна помощь?\n',
                'Что ж, если ты не понял, то у тебя есть клавиатура из кнопок, ',
                'нажав на которые, ты сможешь добиться от меня ответа.']

IDIOMS_LIST = ["𝗖𝗿𝗼𝘀𝘀 𝗺𝘆 𝗵𝗲𝗮𝗿𝘁 𝗮𝗻𝗱 𝗵𝗼𝗽𝗲 𝘁𝗼 𝗱𝗶𝗲(обещать,  клясться)",
               "𝗠𝗮𝗸𝗲 𝗮 𝗳𝗼𝗿𝘁𝘂𝗻𝗲 (очень быстро разбогатеть, приложив к этому минимум усилий)",
               "𝗦𝗽𝗲𝗮𝗸 𝗼𝗳 𝘁𝗵𝗲 𝗱𝗲𝘃𝗶𝗹 (легок на помине, помяни черта, он и появится)",
               "𝗜𝗳 𝘆𝗼𝘂'𝗹𝗹 𝗽𝗮𝗿𝗱𝗼𝗻 𝗺𝘆 𝗙𝗿𝗲𝗻𝗰𝗵 (Простите мой французский/меня за мой французский)",
               "𝗕𝗿𝗲𝗮𝗸 𝗮 𝗹𝗲𝗴 (Удачи!)",
               "𝗝𝗮𝗰𝗸 𝗼𝗳 𝗮𝗹𝗹 𝘁𝗿𝗮𝗱𝗲𝘀 (мастер на все руки)",
               "𝗔𝗻𝗱 𝗮𝗹𝗹 𝘁𝗵𝗮𝘁 𝗷𝗮𝘇𝘇 (и так далее, и тому подобное)",
               "𝗟𝗼𝘀𝗲 𝘆𝗼𝘂𝗿 𝘁𝗼𝘂𝗰𝗵 (потерять способность/талант к чему-то)",
               "𝗟𝗲𝘁 𝘀𝗹𝗲𝗲𝗽𝗶𝗻𝗴 𝗱𝗼𝗴𝘀 𝗹𝗶𝗲 (не надо дергать тигра за усы, лучше не открывать ящик Пандоры)",
               "𝗠𝗼𝗻𝗸𝗲𝘆 𝗯𝘂𝘀𝗶𝗻𝗲𝘀𝘀 (валяние дурака, размениваться на мелочи)",
               "𝗝𝘂𝗺𝗽 𝗼𝗻 𝘁𝗵𝗲 𝗯𝗮𝗻𝗱𝘄𝗮𝗴𝗼𝗻 (присоединиться к какому-то популярному движению только потому, что так делают другие)",
               "𝗖𝘂𝘁 𝗰𝗼𝗿𝗻𝗲𝗿𝘀 (cделать что-то самым легким, дешевым или быстрым путем (иногда, в ущерб качеству результата), кое-как)"]

EXAMPLES_LIST = [
    "𝐼 𝑑𝑖𝑑 𝑙𝑜𝑐𝑘 𝑡ℎ𝑒 𝑑𝑜𝑜𝑟 — 𝑐𝑟𝑜𝑠𝑠 𝑚𝑦 ℎ𝑒𝑎𝑟𝑡 𝑎𝑛𝑑 ℎ𝑜𝑝𝑒 𝑡𝑜 𝑑𝑖𝑒! (Я правда закрывал дверь, клянусь!)",
    '𝑊𝑎𝑟𝑟𝑒𝑛 𝐵𝑢𝑓𝑓𝑒𝑡𝑡 ℎ𝑎𝑠 𝑚𝑎𝑑𝑒 𝑎 𝑓𝑜𝑟𝑡𝑢𝑛𝑒 𝑜𝑓𝑓 𝐴𝑝𝑝𝑙𝑒 — ℎ𝑒𝑟𝑒’𝑠 𝑡ℎ𝑒 𝑠𝑖𝑚𝑝𝑙𝑒 𝑟𝑒𝑎𝑠𝑜𝑛 ℎ𝑒 𝑖𝑛𝑣𝑒𝑠𝑡𝑒𝑑 𝑖𝑛 𝑖𝑡. (Уоррен Баффет сорвал куш на Apple, вот простая причина того, что он инвестировал в эту компанию.)',
    '𝐷𝑖𝑑 𝑦𝑜𝑢 ℎ𝑒𝑎𝑟 𝑤ℎ𝑎𝑡 ℎ𝑎𝑝𝑝𝑒𝑛𝑒𝑑 𝑡𝑜 𝑀𝑎𝑟𝑦 𝑡𝑜𝑑𝑎𝑦? 𝑂ℎ, 𝑠𝑝𝑒𝑎𝑘 𝑜𝑓 𝑡ℎ𝑒 𝑑𝑒𝑣𝑖𝑙, 𝑡ℎ𝑒𝑟𝑒 𝑠ℎ𝑒 𝑖𝑠. (Ты слышал, что сегодня произошло с Мэри? О, вот и она сама, легка на помине.)',
    '𝐴𝑟𝑒 𝑦𝑜𝑢 𝑘𝑖𝑑𝑑𝑖𝑛𝑔 𝑚𝑒? 𝑇ℎ𝑎𝑡’𝑠 ℎ𝑜𝑟𝑠𝑒𝑠ℎ𝑖𝑡, 𝑖𝑓 𝑦𝑜𝑢’𝑙𝑙 𝑝𝑎𝑟𝑑𝑜𝑛 𝑚𝑦 𝐹𝑟𝑒𝑛𝑐ℎ! (Шутишь? Прости, конечно, за мой французский, но это чушь собачья.)',
    "𝐻𝑎𝑣𝑒𝑛’𝑡 𝐼 𝑡𝑜𝑙𝑑 𝑦𝑜𝑢 𝑡ℎ𝑎𝑡 𝐼'𝑚 𝑔𝑜𝑖𝑛𝑔 𝑡𝑜 𝑞𝑢𝑖𝑡 𝑠𝑚𝑜𝑘𝑖𝑛𝑔? (Разве я не говорил, что бросаю курить?) — 𝑂ℎ, 𝑤𝑜𝑤, 𝑏𝑟𝑒𝑎𝑘 𝑎 𝑙𝑒𝑔! (Ого, удачи!)",
    '𝐼 𝑎𝑚 𝑣𝑒𝑟𝑦 𝑔𝑙𝑎𝑑 𝑡ℎ𝑎𝑡 𝑚𝑦 ℎ𝑢𝑠𝑏𝑎𝑛𝑑 𝑖𝑠 𝑎 𝐽𝑎𝑐𝑘 𝑜𝑓 𝑎𝑙𝑙 𝑡𝑟𝑎𝑑𝑒𝑠; 𝑖𝑡 𝑠𝑎𝑣𝑒𝑑 𝑢𝑠 𝑎 𝑙𝑜𝑡 𝑜𝑓 𝑚𝑜𝑛𝑒𝑦 𝑤ℎ𝑒𝑛 𝑖𝑡 𝑐𝑎𝑚𝑒 𝑡𝑜 𝑟𝑒𝑛𝑜𝑣𝑎𝑡𝑖𝑛𝑔 𝑜𝑢𝑟 ℎ𝑜𝑢𝑠𝑒. («Я очень рада, что мой муж — мастер на все руки. Это помогло нам сэкономить много денег при ремонте дома».)',
    '𝑀𝑦 𝐸𝑛𝑔𝑙𝑖𝑠ℎ 𝑡𝑒𝑎𝑐ℎ𝑒𝑟 𝑖𝑠 𝑠𝑚𝑎𝑟𝑡 𝑎𝑛𝑑 𝑘𝑖𝑛𝑑, 𝑡𝑜𝑙𝑒𝑟𝑎𝑛𝑡 𝑎𝑛𝑑 𝑠𝑒𝑐𝑢𝑟𝑒, 𝑝𝑎𝑡𝑖𝑒𝑛𝑡 𝑎𝑛𝑑 𝑎𝑙𝑙 𝑡ℎ𝑎𝑡 𝑗𝑎𝑧𝑧. (Мой учитель английского умный и добрый, спокойный и уверенный, терпеливый и все такое.)',
    "𝐻𝑒 𝑢𝑠𝑒𝑑 𝑡𝑜 𝑏𝑒 𝑎 𝑔𝑜𝑜𝑑 𝑖𝑙𝑙𝑢𝑠𝑡𝑟𝑎𝑡𝑜𝑟, 𝑏𝑢𝑡 𝐼 𝑡ℎ𝑖𝑛𝑘 ℎ𝑒'𝑠 𝑙𝑜𝑠𝑖𝑛𝑔 ℎ𝑖𝑠 𝑡𝑜𝑢𝑐ℎ. (Раньше он был хорошим иллюстратором, но, думаю, он растерял свой талант.)",
    '𝑆ℎ𝑜𝑢𝑙𝑑 𝐼 𝑠𝑡𝑎𝑟𝑡 𝑤𝑎𝑡𝑐ℎ𝑖𝑛𝑔 𝐺𝑎𝑚𝑒 𝑜𝑓 𝑇ℎ𝑟𝑜𝑛𝑒𝑠 𝑜𝑟 𝑗𝑢𝑠𝑡 𝑙𝑒𝑡 𝑠𝑙𝑒𝑒𝑝𝑖𝑛𝑔 𝑑𝑜𝑔𝑠 𝑙𝑖𝑒? (Мне начать смотреть "Игру престолов", или лучше не открывать ящик Пандоры?',
    "𝐼 𝑑𝑜𝑛'𝑡 ℎ𝑎𝑣𝑒 𝑛𝑜 𝑡𝑖𝑚𝑒 𝑓𝑜𝑟 𝑛𝑜 𝑚𝑜𝑛𝑘𝑒𝑦 𝑏𝑢𝑠𝑖𝑛𝑒𝑠𝑠. (Мне некогда размениваться на мелочи.)",
    "𝑌𝑒𝑎ℎ, 𝐼'𝑚 𝑗𝑢𝑚𝑝𝑖𝑛𝑔 𝑜𝑛 𝑡ℎ𝑒 𝑏𝑎𝑛𝑑𝑤𝑎𝑔𝑜𝑛 𝑡ℎ𝑖𝑠 𝑦𝑒𝑎𝑟 𝑎𝑛𝑑 𝑚𝑎𝑘𝑖𝑛𝑔 𝑎 𝐵𝑒𝑠𝑡 𝑜𝑓 2023 𝑣𝑖𝑑𝑒𝑜 𝑜𝑛 𝑌𝑜𝑢𝑡𝑢𝑏𝑒. (Да, в этом году я поддамся популярным тенденциям и выложу на ютуб видео «Лучшее за 2023».)",
    '𝑇ℎ𝑒𝑟𝑒 𝑖𝑠 𝑎𝑙𝑤𝑎𝑦𝑠 𝑎 𝑡𝑒𝑚𝑝𝑡𝑎𝑡𝑖𝑜𝑛 𝑡𝑜 𝑐𝑢𝑡 𝑐𝑜𝑟𝑛𝑒𝑟𝑠 𝑤ℎ𝑒𝑛 𝑡𝑖𝑚𝑒 𝑖𝑠 𝑠ℎ𝑜𝑟𝑡. (Всегда есть соблазн работать кое-как, когда времени мало.)']

test = {"𝗖𝗿𝗼𝘀𝘀 𝗺𝘆 𝗵𝗲𝗮𝗿𝘁 𝗮𝗻𝗱 𝗵𝗼𝗽𝗲 𝘁𝗼 𝗱𝗶𝗲": "обещать,  клясться",
        "𝗠𝗮𝗸𝗲 𝗮 𝗳𝗼𝗿𝘁𝘂𝗻𝗲": "разбогатеть c минимумом усилий",
        "𝗦𝗽𝗲𝗮𝗸 𝗼𝗳 𝘁𝗵𝗲 𝗱𝗲𝘃𝗶𝗹": "легок на помине",
        "𝗜𝗳 𝘆𝗼𝘂'𝗹𝗹 𝗽𝗮𝗿𝗱𝗼𝗻 𝗺𝘆 𝗙𝗿𝗲𝗻𝗰𝗵": "Простите меня за мой французский",
        "𝗕𝗿𝗲𝗮𝗸 𝗮 𝗹𝗲𝗴": "Удачи!",
        "𝗝𝗮𝗰𝗸 𝗼𝗳 𝗮𝗹𝗹 𝘁𝗿𝗮𝗱𝗲𝘀": "мастер на все руки",
        "𝗔𝗻𝗱 𝗮𝗹𝗹 𝘁𝗵𝗮𝘁 𝗷𝗮𝘇𝘇": "и так далее, и тому подобное",
        "𝗟𝗼𝘀𝗲 𝘆𝗼𝘂𝗿 𝘁𝗼𝘂𝗰𝗵": "потерять способность к чему-то",
        "𝗟𝗲𝘁 𝘀𝗹𝗲𝗲𝗽𝗶𝗻𝗴 𝗱𝗼𝗴𝘀 𝗹𝗶𝗲": "не открывать ящик Пандоры",
        "𝗠𝗼𝗻𝗸𝗲𝘆 𝗯𝘂𝘀𝗶𝗻𝗲𝘀𝘀": "валяние дурака",
        "𝗝𝘂𝗺𝗽 𝗼𝗻 𝘁𝗵𝗲 𝗯𝗮𝗻𝗱𝘄𝗮𝗴𝗼𝗻": "присоединиться к поп движению",
        "𝗖𝘂𝘁 𝗰𝗼𝗿𝗻𝗲𝗿𝘀": "cделать что-то самым легким путем"}

SKOLKO_IDIOM = len(IDIOMS_LIST)
SKOLKO_EXAMPLE = SKOLKO_IDIOM

game_started = False

chosen_quest = ''
r_ans = ''


def current_weather(lat, lon):
    url = f'https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m,apparent_temperature,precipitation,rain,showers,snowfall,weather_code,wind_speed_10m,wind_direction_10m&wind_speed_unit=ms&timezone=Europe%2FMoscow'
    r = requests.get(url).json()['current']
    ans = f"Температура: {r['temperature_2m']} °C\nСкорость ветра: {r['wind_speed_10m']} м/с\n"
    lst = ['С', 'CB', 'B', 'ЮВ', 'Ю', 'ЮЗ', 'З', "СЗ"]
    win_dir = lst[r['wind_direction_10m'] % 360 // 45]
    ans += f'Направление ветра: {win_dir}'
    w_code = {
        0: "Ясное небо",
        1: "В основном ясно",
        2: 'Частично облачно',
        3: 'Пасмурно',
        45: "Туман",
        48: 'осаждающий иней, туман',
        51: 'Легкий моросящий дождь',
        53: 'Умеренный моросящий дождь',
        55: 'Моросящий дождь густой интенсивности',
        56: 'Mоросящий мелкий дождик',
        57: 'Моросящий густой и интенсивный дождь',
        61: 'Небольшой дождь',
        63: 'Дождь умеренный',
        65: 'Дождь сильной интенсивности',
        66: 'Мелкий ледяной дождь',
        67: "Ледяной сильный дождь",
        71: 'Небольшой снегопад',
        73: 'Умеренный снегопад',
        75: 'Сильный снегопад',
        77: 'Снежные зёрна',
        80: 'Небольшой ливень',
        81: 'Умеренный ливень',
        82: 'Сильные ливневые дожди',
        85: 'Небольшой сильный снегопад',
        86: 'Сильный снегопад',
        95: 'Небольшая гроза',
        96: 'Гроза с небольшим градом',
        99: 'Гроза с сильным градом'
    }
    weather_status = w_code[r['weather_code']]
    ans += f'\nСостояние погоды: {weather_status}'
    return ans


lat = '52.52'
lon = '13.41'


def start_menu():
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    button = telebot.types.KeyboardButton(text='Случайный анекдот')
    keyboard.add(button)


users_info = {}  # Здесь будет храниться информация о игроке

joke = {"programming": [
    'У меня была одна проблема, поэтому я решил написать программу, которая её решит. Теперь у меня есть 1 проблема, 9 ошибок и 12 предупреждений.',
    'Если бы программисты были врачами, им бы говорили «У меня болит нога», а они отвечали «Ну не знаю, у меня такая же нога, а ничего не болит»',
    'Хороший программист проливает кофе на себя. И ноут цел, и бодрит в два раза лучше.',
    'Не переживай, если не все работает как надо. Если бы все работало хорошо, то ты бы здесь давно уже не работал.',
    'Баг — это еще не записанная  фича.',
    'Основные изменения в новой версии программы: исправлены старые баги, добавлены новые.'
],
    'gamers': [
        'Девушки! Если парень останавливает видеоигру, чтобы ответить на ваше сообщение, — выходите за него замуж!',
        'Сейчас нужно очень внимательно переходить дорогу, так как дети, выросшие на GTA, Carmageddon и Need For Speed, начали получать водительские права.',
        'Интересно, если я продам аккаунт сына и мужа в «Танках» и куплю себе путевку на море, я до вокзала доехать успею?',
        'Если так подумать, то, когда ты тратишь деньги на шмотки и прочие бонусы в играх, чтобы быстрее победить, ты, по сути, платишь за то, чтобы меньше играть.🙁',
        '— Какой у тебя уровень IQ? \n— Я не играл в эту игру.',
    ],
    'stirlitz': [
        'Штирлиц играл в карты и проигрался. Но Штирлиц умел делать хорошую мину при плохой игре. Когда Штирлиц покинул компанию, мина сработала.',
        'Штирлицу попала в голову пуля. "Разрывная," - раскинул мозгами Штирлиц.',
        'Штирлиц долго смотрел в одну точку. Потом в другую. "Двоеточие!" - наконец-то смекнул Штирлиц.',
        'Письмо из центра до Штиpлица не дошло... Пришлось читать во второй раз.']
}

locations = {
    '1': {'text': 'Вы играете за героя, который попал в опасный лес. Вам нужно выбраться живым.',
          'items': [],
          'next_move': {'Пойти вперед': '2'},
          'exchange': {}},
    '2': {'text': 'Вы попали в самую чащу леса. Тут очень тихо.',
          'items': [],
          'next_move': {'Пойти налево': '3', 'Пойти прямо': '4', 'Пойти направо': '5'},
          'exchange': {}},
    '3': {
        'text': 'Вы забрели в самую темную и зловещую часть леса. В темноте вы не заметили маленькую ядовитую змею. Вас укусили. Вы отправились к праотцам.\n(можешь выбрать другой вариант в моём предыдущем сообщении и как будто ничего не было😊)',
        'items': [],
        'next_move': {},
        'exchange': {}},
    '4': {
        'text': 'Вы вышли на поле. Перед вами стоит торговец. Он предложил вам 3 золотых монет за шкатулку. Однако у вас её нет',
        'items': [],
        'next_move': {'Вернуться обратно': '2'},
        'exchange': {'шкатулка': 'золото: 3'}},
    '5': {'text': 'Вы оказались около зловещего подземелья.',
          'items': [],
          'next_move': {'Пойти назад': '2', 'Пойти внутрь': '7', 'Осмотреться вокруг': '6'},
          'exchange': {}},
    '6': {
        'text': 'Вы бродите рядом с пещерой в надежде найти что-то интересное...И вам улыбается удача: вы нашли шкатулку!',
        'items': ['шкатулка'],
        'next_move': {'Вернуться к подземелью': '5'},
        'exchange': {}},
    '7': {
        'text': 'Стены здесь из грубого камня и покрыты мхом и плесенью. Вы чувствуете запах сырости и одиночества.\nОпустив глаза на пол, вы увидели 2 золотые монеты, лежащие в углу под потухшим факелом. Разумеется, вы не прошли мимо них.',
        'items': ['золото: 2'],
        'next_move': {'Пойти вперед': '8', 'Выйти на улицу': '5'},
        'exchange': {}},
    '8': {'text': 'Вы проходите дальше. Тут очень темно, но вдруг вы замечаете свет...',
          'items': [],
          'next_move': {'Пойти дальше': '9', 'Вернуться': '7'},
          'exchange': {}},
    '9': {'text': 'Выход уже близко, но придется заплатить.',
          'items': [],
          'next_move': {'Вернуться назад': '8'},
          'exchange': {'золото: 5': 'выход'}}
}


def generate_story(user, position, call=None):
    # Берем текстовое описание локации
    txt = locations[position]['text']
    # Меняем текстовое описание локации при условии тех или иных выполненных игроком действий
    if users_info[user]['shkatulka_taken'] and position == '6':
        txt = "Вы уже подобрали шкатулку. Больше здесь ничего интересного нет."
    if users_info[user]['items'] == ['шкатулка'] and position == '4':
        txt = 'Вы вышли на поле. Перед вами стоит торговец. Он предложил вам 3 золотых монет за шкатулку. У вас есть шкатулка, поэтому вы согласились.'
    if position == '4' and users_info[user]['shkatulka_given'] == True:
        txt = 'Вы уже обменяли шкатулку у торговца, больше ему нечего вам предложить.'
    if position == '7' and users_info[user]['coins_taken'] == True:
        txt = 'Стены здесь из грубого камня и покрыты мхом и плесенью. Вы чувствуете запах сырости и одиночества.\nВы уже подобрали лежавшие в углу монеты, так что можете идти дальше'
    # Создаём клавиатуру
    keyboard = telebot.types.InlineKeyboardMarkup()
    # cоздаём кнопки с возмодными ходами
    for i in users_info[user]['loc'][position]['next_move']:
        # берём текст направления
        key_text = i
        # берем название локации
        key_data = locations[position]['next_move'][i]
        # Добавляем кнопки в клавиатуру
        keyboard.add(telebot.types.InlineKeyboardButton(text=key_text, callback_data=key_data))
    # Проверяем условия для подбирания или обмена предметов
    if users_info[user]['loc'][users_info[user]['cur_pos']]['items'] and \
            users_info[user]['loc'][users_info[user]['cur_pos']]['items'] != ['золото: 2'] and not users_info[user][
        'shkatulka_taken']:
        users_info[user]['items'] = users_info[user]['loc'][users_info[user]['cur_pos']]['items']
        users_info[user]['shkatulka_taken'] = True
    if users_info[user]['loc'][users_info[user]['cur_pos']]['items'] == ['золото: 2']:
        users_info[user]['coins'] += int(users_info[user]['loc'][users_info[user]['cur_pos']]['items'][0][-1])
        users_info[user]['coins_taken'] = True
    if users_info[user]['loc'][users_info[user]['cur_pos']]['exchange'] and users_info[user]['items'] and \
            users_info[user]['cur_pos'] not in ['7', '8', '9']:
        users_info[user]['coins'] += int(
            users_info[user]['loc'][users_info[user]['cur_pos']]['exchange'][users_info[user]['items'][0]][-1])
        users_info[user]['shkatulka_given'] = True
    if users_info[user]['loc'][users_info[user]['cur_pos']]['exchange'] == {'золото: 5': 'выход'}:
        if users_info[user]['coins'] >= 5:
            bot.send_message(call.message.chat.id,
                             'У вас достаточно денег, чтобы покинуть это место. Вы наконец свободны!')
            users_info[user]['good_endings'] += 1
            return None, None
    if users_info[user]['cur_pos'] == '3':
        users_info[user]['bad_endings'] += 1
    if users_info[user]['cur_pos'] == '6':
        users_info[user]['shkatulka_taken'] = True
    # Отправляем текст и клавиатуру
    return (txt, keyboard)


def start_game(message):
    # Добавляем пользователя в словарь со значениями по умолчанию
    users_info[message.from_user.username] = {'cur_pos': '1',
                                              'coins': 0,
                                              'items': [],
                                              'loc': deepcopy(locations),
                                              'bad_endings': 0,
                                              'good_endings': 0,
                                              'shkatulka_taken': False,
                                              'shkatulka_given': False,
                                              'coins_taken': False}
    # Генерируем уровень игры
    txt, keyboard = generate_story(message.from_user.username, users_info[message.from_user.username]['cur_pos'])
    bot.send_message(message.chat.id, txt, reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data in locations)
def callback_query(call):
    # меняем текущую позицию пользователя
    users_info[call.from_user.username]['cur_pos'] = call.data
    # генерируем новый текст и кнопки
    txt, keyboard = generate_story(call.from_user.username, users_info[call.from_user.username]['cur_pos'], call=call)
    # Отправляем сообщение с новыми кнопкмми и текстом
    if txt and keyboard:
        bot.send_message(call.message.chat.id, txt, reply_markup=keyboard)


# Функция, запрашивающая местоположение пользователя
def weather(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button_geo = telebot.types.KeyboardButton(text='Поделиться местоположением', request_location=True)
    keyboard.add(button_geo)
    bot.send_message(message.chat.id, 'Поделись местоположением', reply_markup=keyboard)


@bot.message_handler(content_types=['location'])
def location(message):
    a = telebot.types.ReplyKeyboardRemove()
    bot.send_message(message.chat.id, current_weather(message.location.latitude, message.location.longitude),
                     reply_markup=a)
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    button = telebot.types.KeyboardButton(text='Сыграть в игру')
    button2 = telebot.types.KeyboardButton(text='Погода у меня')
    button3 = telebot.types.KeyboardButton(text='Случайный анекдот😆')
    button4 = telebot.types.KeyboardButton(text='Случайная фотография котика')
    button5 = telebot.types.KeyboardButton(text='Случайное число')
    button6 = telebot.types.KeyboardButton(text='Установить таймер')
    button7 = telebot.types.KeyboardButton(text='Сыграть в камень ножницы бумага')
    button8 = telebot.types.KeyboardButton(text='Учить идиомы')
    keyboard.add(button, button2, button3, button4, button5, button6, button7, button8)
    bot.send_message(message.chat.id, 'Ну что, чем займёмся теперь?', reply_markup=keyboard)


def send_joke(mess, theme):
    result = random.choice(joke[theme])
    bot.send_message(mess.message.chat.id, result)


def start_anek(message):
    bot.send_chat_action(message.chat.id, "typing", timeout=10)
    keyboard = telebot.types.InlineKeyboardMarkup()
    but1 = telebot.types.InlineKeyboardButton("Про программистов", callback_data="programming")
    but2 = telebot.types.InlineKeyboardButton("Про геймеров", callback_data='gamers')
    but3 = telebot.types.InlineKeyboardButton('Про Штрилица😁', callback_data='stirlitz')
    keyboard.add(but1, but2, but3)
    bot.send_message(message.chat.id, "А на какую тему анекдот-то?", reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data in ['programming', 'gamers', 'stirlitz'])
def joke_callback(call):
    send_joke(call, call.data)


def send_rand_cat(message):
    r = requests.get('https://cataas.com/cat?json=true')
    try:
        url = 'https://cataas.com/cat/' + r.json()['_id']
        bot.send_photo(message.chat.id, url)
    except requests.exceptions.JSONDecodeError:
        bot.send_message(message.chat.id, 'Упс, извини, кажется, какие-то проблемы с сайтом. Я тут точно ни при чём😇')


def send_cat_text(message):
    msg = bot.send_message(message.chat.id, 'Придумай подпись и напиши её мне')
    bot.register_next_step_handler(msg, send_photo_text)


def send_photo_text(message):
    r = requests.get('https://cataas.com/cat/says/' + message.text + '?json=true')
    try:
        url = 'https://cataas.com/cat/' + r.json()['_id'] + f'/says/{message.text}'
        bot.send_photo(message.chat.id, url)
    except requests.exceptions.JSONDecodeError:
        bot.send_message(message.chat.id, 'Упс, извини, кажется, какие-то проблемы с сайтом. Я тут точно ни при чём😇')


# Функция, отправляющая рандомное число в диапазоне, заданном пользователем
def random_num(message):
    try:
        aс, bс = int(message.text.split()[0]), int(message.text.split()[1])
    except ValueError:
        if not "Случай" in message.text:
            bot.send_message(message.chat.id,
                             f'Ну, раз ты не хочешь по своему, будет по-моему! Мое число:{random.choice([1337, 148480, 1552, 1234])}')
        else:
            bot.send_message(message.chat.id,
                             f'Что, неужели так сложно написать два числа? Хорошо, вот тебе моё случайное число:{random.randint(0, 10 ** 10)}')
        return
    if bс > aс:
        bot.send_message(message.chat.id, f'Вот тебе случайное число от {aс} до {bс}: {random.randint(aс, bс)}')
    elif aс == bс:
        bot.send_message(message.chat.id,
                         'Ну и зачем ты отправил два одинаковых числа?😡 Думаешь, это смешно? Вовсе нет!')
    else:
        bot.send_message(message.chat.id,
                         f'Ага, хотел перехитрить меня? Думал, что я сломаюсь? А вот и нет! Моё число от {bс} до {aс}: {random.randint(bс, aс)}')


@bot.message_handler(content_types=['sticker'])
def get_sticker(message):
    bot.send_message(message.chat.id,
                     f'Классный стикер! Кстати, знаешь его ID? Я вот знаю. Вот он: {message.sticker.file_id}')


@bot.message_handler(commands=['help'])
def help(message):
    h_mes = ''
    for i in help_message:
        h_mes += i
    bot.send_message(message.chat.id, h_mes)


user_data = {}


# Обработчик команды /reminder
def reminder_message(message):
    # Запрашиваем у пользователя название напоминания и дату и время напоминания
    bot.send_message(message.chat.id,
                     'Что именно я должен тебе напомнить?: (/cancel_timer, если захочешь отменить таймер)')
    bot.register_next_step_handler(message, set_reminder_name)


# Функция, которую вызывает обработчик команды /reminder для установки названия напоминания
def set_reminder_name(message):
    user_data[message.chat.id] = {'reminder_name': message.text}
    user_data[message.chat.id]['timer'] = []
    bot.send_message(message.chat.id,
                     'Когда напомнить? Введи дату и время в формате ГГГГ-ММ-ДД чч:мм:сс.')
    bot.register_next_step_handler(message, reminder_set, user_data)


# Функция, которую вызывает обработчик команды /reminder для установки напоминания
def reminder_set(message, user_data):
    try:
        # Преобразуем введенную пользователем дату и время в формат datetime
        reminder_time = datetime.datetime.strptime(message.text, '%Y-%m-%d %H:%M:%S')
        now = datetime.datetime.now()
        delta = reminder_time - now
        # Если введенная пользователем дата и время уже прошли, выводим сообщение об ошибке
        if delta.total_seconds() <= 0:
            bot.send_message(message.chat.id, 'Я не машина времени, поставь дату, которая ешё не прошла')
            bot.register_next_step_handler(message, reminder_set, user_data)
        # Если пользователь ввел корректную дату и время, устанавливаем напоминание и запускаем таймер
        else:
            reminder_name = user_data[message.chat.id]['reminder_name']
            bot.send_message(message.chat.id,
                             'Напоминание "{}" успешно установлено на {}.'.format(reminder_name, reminder_time))
            reminder_timer = threading.Timer(delta.total_seconds(), send_reminder, [message.chat.id, reminder_name])
            reminder_timer.start()
            user_data[message.chat.id]['timer'].append(reminder_timer)
    # Если пользователь ввел некорректную дату и время, выводим сообщение об ошибке
    except ValueError:
        bot.send_message(message.chat.id, 'Ошибка! Неверный формат даты и времени, попробуй-ка еще раз.')
        bot.register_next_step_handler(message, reminder_set, user_data)


# Функция, которая отправляет напоминание пользователю
def send_reminder(chat_id, reminder_name):
    bot.send_message(chat_id, f'Время получить напоминание "{reminder_name}"!')


def idioms(message):
    bot.send_message(message.chat.id,
                     'Ага! Неужели наконец-то за голову взялся? Ну хорошо, сейчас мы с тобой поучим английские идиомы.')
    for i in range(3, SKOLKO_IDIOM + 1, 3):
        stroka = ''
        idis = [IDIOMS_LIST[i - 3], IDIOMS_LIST[i - 2], IDIOMS_LIST[i - 1]]
        exes = [EXAMPLES_LIST[i - 3], EXAMPLES_LIST[i - 2], EXAMPLES_LIST[i - 1]]
        for y in range(len(idis)):
            stroka += f'{idis[y]} \nПример: {exes[y]} \n \n'
        bot.send_message(message.chat.id, stroka)
    bot.send_message(message.chat.id, 'Ну, как-то так🙃. Теперь дело за тобой.')

def english_test(message):
    global chosen_quest, r_ans
    a = list(test.keys())
    b = list(test.values())
    n_idim = random.choice(a)
    chosen_quest = n_idim
    r_ans = test[n_idim]
    w1_ans = random.choice(b)
    w2_ans = random.choice(b)
    while not(r_ans != w1_ans and r_ans != w2_ans and w1_ans != w2_ans):
        w1_ans = random.choice(b)
        w2_ans = random.choice(b)
    keybord = telebot.types.InlineKeyboardMarkup()
    button = telebot.types.InlineKeyboardButton(text=w1_ans, callback_data=w1_ans)
    button2 = telebot.types.InlineKeyboardButton(text=r_ans, callback_data=r_ans)
    button3 = telebot.types.InlineKeyboardButton(text=w2_ans, callback_data=w2_ans)
    sp = [button, button2, button3]
    random.shuffle(sp)
    for i in sp:
        keybord.add(i)
    bot.send_message(message.chat.id, f'Выбери правильный вариант перевода идиомы: {n_idim}', reply_markup=keybord)

@bot.callback_query_handler(func=lambda call: call.data in test.values())
def check_ans(call):
    global chosen_quest
    if list(test.keys()).index(chosen_quest) == list(test.values()).index(call.data):
        bot.send_message(call.message.chat.id, 'Правильно! Продолжай в том же духе!')
    else:
        bot.send_message(call.message.chat.id, f'Неверно! Правильный ответ:{r_ans}')
    english_test(call.message)


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Здраствуй! Скорее всего, ты не общался со мной ранее, если уж использовал эту команду, поэтому - рад познакомиться! И кстати, я люблю, когда со мной здороваются, как с человеком, а с ботом😉')


@bot.message_handler(commands=['cancel_timer'])
def cancel_timer(message):
    for i in range(len(user_data[message.chat.id]['timer'])):
        timer = user_data[message.chat.id]['timer'][i]
        timer.cancel()
    bot.send_message(message.chat.id, 'Таймер был успешно сброшен. Можешь не благодарить😎')


# Функция для начала игры в камень-ножницы-бумага
def play_rps(message):
    bot_mes = {'камень': "камень", "ножницы": "ножницы", "бумага": "бумагу"}
    keyboard = telebot.types.InlineKeyboardMarkup()
    but1 = telebot.types.InlineKeyboardButton('Камень', callback_data='Камень')
    but2 = telebot.types.InlineKeyboardButton('Ножницы', callback_data='Ножницы')
    but3 = telebot.types.InlineKeyboardButton('Бумага', callback_data='Бумага')
    keyboard.add(but1, but2, but3)
    bot.send_message(message.chat.id, 'Так что же ты выберешь?', reply_markup=keyboard)


@bot.message_handler(content_types=['text'])
def starting_message(message):
    global game_started
    sad_flag = False
    said_hello = False
    said_goodbye = False
    but_pressed = False
    timer_set = False
    rps_play_started = False
    thanks_said = False
    idioms_started = False
    if 'привет' in message.text or 'Привет' in message.text:
        if not said_hello:
            said_hello = True
            keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
            button = telebot.types.KeyboardButton(text='Сыграть в игру')
            button2 = telebot.types.KeyboardButton(text='Погода у меня')
            button3 = telebot.types.KeyboardButton(text='Случайный анекдот😆')
            button4 = telebot.types.KeyboardButton(text='Случайная фотография котика')
            button5 = telebot.types.KeyboardButton(text='Случайное число')
            button6 = telebot.types.KeyboardButton(text='Установить таймер')
            button7 = telebot.types.KeyboardButton(text='Сыграть в камень ножницы бумага')
            button8 = telebot.types.KeyboardButton(text='Учить идиомы')
            keyboard.add(button, button2, button3, button4, button5, button6, button7, button8)
            bot.send_message(message.chat.id,
                             'И тебе привет!🙋🏻‍♂️ Смотри, что я умею.\nКстати, если нужна помощь, пропиши команду /help, и я тебе всё расскажу.',
                             reply_markup=keyboard)
        else:
            bot.send_message(message.chat.id, 'Поздорвались уже😑')
    elif 'пока' in message.text or "Пока" in message.text:
        said_goodbye = True
        a = telebot.types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id, "Пока-пока! Жду тебя снова!",
                         reply_markup=a)
    elif 'Сыграть в игру' in message.text:
        but_pressed = True
        game_started = True
        start_game(message)
    elif 'Погода у меня' in message.text:
        but_pressed = True
        weather(message)
    elif 'Случайный анекдот😆' in message.text:
        but_pressed = True
        start_anek(message)
    elif 'Случайная фотография котика' in message.text:
        but_pressed = True
        keyboard52 = telebot.types.InlineKeyboardMarkup()
        but1 = telebot.types.InlineKeyboardButton("С подписью", callback_data="подпись")
        but2 = telebot.types.InlineKeyboardButton("Без подписи", callback_data='без подписи')
        keyboard52.add(but1, but2)
        bot.send_message(message.chat.id, "С подписью или без?", reply_markup=keyboard52)
    elif 'Случайное число' in message.text:
        but_pressed = True
        msg = bot.send_message(message.chat.id, "От какого числа до какого? Напиши 2 числа")
        bot.register_next_step_handler(msg, random_num)
    elif 'Установить таймер' in message.text:
        timer_set = True
        reminder_message(message)
    elif 'Сыграть в камень ножницы бумага' in message.text:
        play_rps(message)
        rps_play_started = True
    elif 'Учить идиомы' in message.text:
        idioms_started = True
        keyboard52 = telebot.types.InlineKeyboardMarkup()
        but1 = telebot.types.InlineKeyboardButton("Хочу пройти тест", callback_data="Тест")
        but2 = telebot.types.InlineKeyboardButton("Хочу подучить идиомы", callback_data='Обучение')
        keyboard52.add(but1, but2)
        bot.send_message(message.chat.id, "Хочешь проверить свои знания идиом? Или улучшить их?", reply_markup=keyboard52)

    elif 'Спасибо' in message.text or 'спасибо' in message.text:
        bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAICimYqRDIIn2dIw2mPuREwakyk3-F0AAJUAQACe04qEHOJG1Z2_0xWNAQ')
        bot.send_message(message.chat.id, 'Пожалуйста')
        thanks_said = True
    for i in message.text.split():
        if i in sad_words and (
                'Я' in message.text or 'я' in message.text or 'Мне' in message.text or 'мне' in message.text):
            s_mes = ''
            for i in sad_caption:
                s_mes += i
            bot.send_message(message.chat.id, s_mes)
            sad_flag = True
    else:
        if (not sad_flag and not said_hello and not said_goodbye
                and not but_pressed and not timer_set and not rps_play_started and not thanks_said and not idioms_started):
            bot.send_message(message.chat.id,
                             'Не понял, что ты имеешь ввиду😶‍🌫️\nЛучше напиши "привет", это слово я понимаю')


@bot.callback_query_handler(func=lambda call: call.data == "подпись" or call.data == 'без подписи')
def cat_photo(call):
    if call.data == "подпись":
        send_cat_text(call.message)
    elif call.data == 'без подписи':
        send_rand_cat(call.message)

@bot.callback_query_handler(func=lambda call: call.data == "Тест" or call.data == 'Обучение')
def english(call):
    if call.data == 'Обучение':
        idioms(call.message)
    else:
        bot.send_message(call.message.chat.id, 'Отлично! Приготовься показать мне всё, что знаешь!')
        english_test(call.message)


@bot.callback_query_handler(func=lambda call: call.data in ["Камень", "Ножницы", "Бумага"])
def rps_decider(call):
    bot_mes = {'Камень': "Камень", "Ножницы": "Ножницы", "Бумага": "Бумагу"}
    user_choice = call.data
    bot_choice = random.choice(['Камень', 'Ножницы', 'Бумага'])
    if user_choice == bot_choice:
        bot.send_message(call.message.chat.id, f"Ничья! Я выбрал {bot_mes[bot_choice]}.")
    elif (user_choice == 'Камень' and bot_choice == 'Ножницы') or (
            user_choice == 'Ножницы' and bot_choice == 'Бумага') or (
            user_choice == 'Бумага' and bot_choice == 'Камень'):
        bot.send_message(call.message.chat.id, f"Ты победил! Я выбрал {bot_mes[bot_choice]}.")
    else:
        bot.send_message(call.message.chat.id, f"Я победил! Я выбрал {bot_mes[bot_choice]}.")


if __name__ == "__main__":
    bot.infinity_polling()  # Запускаем скрипт, иначе бот будет молчать
