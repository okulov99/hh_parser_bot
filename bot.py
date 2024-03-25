import telebot
from telebot import types
import csv
from main import save_data_csv, get_vacancies, save_data_json

bot = telebot.TeleBot('TOKEN')

params = {
    "text": 'Официант',
    "area": 1,
    "per_page": 30
}

keyboard1 = types.ReplyKeyboardMarkup(True)


@bot.message_handler(commands=['start'])
def menu(message):
    key = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_1 = types.KeyboardButton(text="Изменить город")
    btn_2 = types.KeyboardButton(text="Изменить название")
    btn_3 = types.KeyboardButton(text="Выбрать количество вакансий")
    btn_4 = types.KeyboardButton(text="Начать парсинг")
    key.add(btn_1, btn_2, btn_3, btn_4)
    bot.send_message(message.chat.id, 'Выберите нужную операцию', reply_markup=key)


@bot.message_handler(content_types=['text'])
def check_message(message):
    if message.text == 'Начать парсинг':
        pars(message)
    elif message.text == 'Изменить город':
        get_vacancy_area(message)
    elif message.text == 'Изменить название':
        get_vacancy_title(message)
    elif message.text == 'Выбрать количество вакансий':
        get_vacancy_amount(message)
    else:
        bot.send_message(message.from_user.id, 'Неизвестная команда')


def get_vacancy_area(message):
    key = types.InlineKeyboardMarkup()
    btn_1 = types.InlineKeyboardButton(text="Москва", callback_data="moscow")
    btn_2 = types.InlineKeyboardButton(text="Санкт-Петербург", callback_data="spb")
    btn_3 = types.InlineKeyboardButton(text="Екатеринбург", callback_data="ekb")
    key.add(btn_1, btn_2, btn_3)
    bot.send_message(message.chat.id, 'Выберите город', reply_markup=key)


@bot.callback_query_handler(func=lambda callback: callback.data)
def check_area_callback(callback):
    global params
    if callback.data == 'moscow':
        params['area'] = 1
    elif callback.data == 'spb':
        params['area'] = 2
    elif callback.data == 'ekb':
        params['area'] = 3
    bot.send_message(callback.from_user.id, 'Изменения сохранены')


def get_vacancy_amount(message):
    msg = bot.send_message(message.from_user.id, 'Укажите количество вакансий', reply_markup=keyboard1)
    bot.register_next_step_handler(msg, save_vacancy_amount)


def save_vacancy_amount(message):
    global params
    if message.text.isdigit():
        params['per_page'] = int(message.text)
        bot.send_message(message.from_user.id, 'Изменения сохранены')
    else:
        bot.send_message(message.from_user.id, 'Должно быть число, попробуйте ещё раз')
        get_vacancy_amount(message)


def get_vacancy_title(message):
    msg = bot.send_message(message.from_user.id, 'Введите название вакансии', reply_markup=keyboard1)
    bot.register_next_step_handler(msg, save_vacancy_title)


def save_vacancy_title(message):
    global params
    if len(message.text) <= 1 or len(message.text) > 30:
        bot.send_message(message.from_user.id, 'Некорректное значение, попробуйте ещё раз')
        get_vacancy_title(message)
    else:
        params['text'] = message.text
        bot.send_message(message.from_user.id, 'Изменения сохранены')


def pars(message):
    save_data_csv(get_vacancies(params))
    bot.send_document(message.chat.id, open(r"C:\projects\headhunter_parser\data.csv", 'rb'))
    save_data_json(get_vacancies(params))
    bot.send_document(message.chat.id, open(r"C:\projects\headhunter_parser\data.json", 'rb'))


bot.polling(none_stop=True)
