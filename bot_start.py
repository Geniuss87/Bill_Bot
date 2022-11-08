import telebot
from decouple import config
from telebot import types
from bs4 import BeautifulSoup
import requests

URL = "https://www.accuweather.com/ru/kg/bishkek/222844/weather-forecast/222844"
HEADERS = {
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36",
    "accept": "*/*",
}


def get_html(url, headers):
    response = requests.get(URL, headers=HEADERS)
    return response


def get_content_from_html(html_text):
    soup = BeautifulSoup(html_text, "html.parser")
    items = soup.find_all("div", class_="page-column-1")
    weather = []
    for item in items:
        weather.append(
            {
                "Температура воздуха": item.find("div", class_="temp").get_text().replace("", ""),
                "Осадки": item.find_next("span", class_="phrase").get_text().replace("", ""),
                "Качество воздуха": item.find_next("p", class_="category-text").get_text().replace("", ""),

            }
        )
    return '\n'.join([f'{key}: {value}' for key, value in weather[0].items()])


def get_result_parse():
    global result
    html = get_html(URL, HEADERS)
    if html.status_code == 200:
        result = get_content_from_html(html.text)
    return result


bot = telebot.TeleBot(config("TOKEN_BOT"))


@bot.message_handler(commands=["start"])
def get_start_msg(msg):
    full_name = f"{msg.from_user.last_name} {msg.from_user.first_name}"
    text = f"Привет {full_name} я бот который поможет рассчитать счет за электроэгнергию. " \
           f"Наберите 'меню' чтобы вызвать МЕНЮ или наберите 'погода' если хотите узнать температуру воздуха за окном"
    bot.send_message(msg.chat.id, text)


@bot.message_handler(content_types=["text"])
def get_msg(msg):
    global a
    markup = types.InlineKeyboardMarkup(row_width=2)
    if msg.text.lower() == "погода":
        text = get_result_parse()
        a = 7
        bot.send_message(msg.chat.id, text, reply_markup=markup)
    if msg.text.lower() == "меню":
        text = "Выберите тип потребителя:"
        btn_1 = types.InlineKeyboardButton("Физлицо", callback_data="fl")
        btn_2 = types.InlineKeyboardButton("Юрлицо", callback_data="ul")
        btn_3 = types.InlineKeyboardButton("Действущие тарифы", callback_data="", url="http://cbd.minjust.gov.kg/act/view/ky-kg/158785/45?cl=ru-ru&mode=tekst")
        markup.add(btn_1, btn_2, btn_3)
        bot.send_message(msg.chat.id, text, reply_markup=markup)
        a = 0
    if msg.text == "Обычный":
        text = "Введите количество дней и количество потребленной электроэнергии в следующем формате: Дни#кВтч (пример 30#700)"
        bot.send_message(msg.chat.id, text, reply_markup=markup)
        a = 1
    if msg.text == "Высокогорник":
        text = "Введите количество дней и количество потребленной электроэнергии в следующем формате: Дни#кВтч (пример 30#1000)"
        bot.send_message(msg.chat.id, text, reply_markup=markup)
        a = 2
    if msg.text == "Небытовой":
        text = "Введите количество потребленной электроэнергии в следующем формате: #кВтч (пример #1000)"
        bot.send_message(msg.chat.id, text, reply_markup=markup)
        a = 3
    if msg.text == "Насос, религиия, троллейбус":
        text = "Введите количество потребленной электроэнергии в следующем формате: #кВтч (пример #1000)"
        bot.send_message(msg.chat.id, text, reply_markup=markup)
        a = 4
    if msg.text == "Злоторудный":
        text = "Введите количество потребленной электроэнергии в следующем формате: #кВтч (пример #1000)"
        bot.send_message(msg.chat.id, text, reply_markup=markup)
        a = 5
    if msg.text == "Цемзавод":
        text = "Введите количество потребленной электроэнергии в следующем формате: #кВтч (пример #1000)"
        bot.send_message(msg.chat.id, text, reply_markup=markup)
        a = 6
    if a == 1 and msg.text.find("#") != -1:
        kwt = msg.text.split("#")
        if int(kwt[1]) / int(kwt[0]) <= 23.0137:
            som = str(round(int(kwt[1]) * 0.77, 2))
            bot.send_message(msg.chat.id, f'{kwt[1]} кВтч * 0.77 сом = {som} сом', reply_markup=markup)
        else:
            som_1 = round(((int(kwt[0]) * 23.0137) * 0.77), 2)
            som_2 = round(((int(kwt[1]) - (int(kwt[0]) * 23.0137)) * 2.16), 2)
            som = str(round(som_1, 2) + round(som_2, 2))
            bot.send_message(msg.chat.id, f'{round((int(kwt[0]) * 23.0137), 2)} кВтч * 0.77 сом = {som_1} сом по '
                                          f'соцнорме, {round((int(kwt[1]) - (int(kwt[0]) * 23.0137)), 2)} кВтч * 2.16 '
                                          f'сом = {som_2} сом свыше нормы, ИТОГО {som} сом',
                             reply_markup=markup)
    if a == 2 and msg.text.find("#") != -1:
        kwt = msg.text.split("#")
        if int(kwt[1]) / int(kwt[0]) <= 32.8767:
            som = str(round(int(kwt[1]) * 0.77, 2))
            bot.send_message(msg.chat.id, f'{kwt[1]} кВтч * 0.77 сом = {som} сом', reply_markup=markup)
        else:
            som_1 = round(((int(kwt[0]) * 32.8767) * 0.77), 2)
            som_2 = round(((int(kwt[1]) - (int(kwt[0]) * 32.8767)) * 2.16), 2)
            som = som_1 + som_2
            bot.send_message(msg.chat.id, f'{round((int(kwt[0]) * 32.8767), 2)} кВтч * 0.77 сом = {som_1} сом по '
                                          f'соцнорме, {round((int(kwt[1]) - (int(kwt[0]) * 32.8767)), 2)} кВтч * 2.16 '
                                          f'сом = {som_2} сом свыше нормы, ИТОГО {round(som, 2)} сом',
                             reply_markup=markup)
    if a == 3 and msg.text.find("#") != -1:
        kwt = msg.text.split("#")
        bot.send_message(msg.chat.id, f'{kwt[1]} кВтч * 2.52 сом = {int(kwt[1]) * 2.52} сом', reply_markup=markup)
    if a == 4 and msg.text.find("#") != -1:
        kwt = msg.text.split("#")
        bot.send_message(msg.chat.id, f'{kwt[1]} кВтч * 1.68 сом = {int(kwt[1]) * 1.68} сом', reply_markup=markup)
    if a == 5 and msg.text.find("#") != -1:
        kwt = msg.text.split("#")
        bot.send_message(msg.chat.id, f'{kwt[1]} кВтч * 5.04 сом = {int(kwt[1]) * 5.04} сом', reply_markup=markup)
    if a == 6 and msg.text.find("#") != -1:
        kwt = msg.text.split("#")
        bot.send_message(msg.chat.id, f'{kwt[1]} кВтч * 3.276 сом = {int(kwt[1]) * 3.276} сом', reply_markup=markup)



@bot.callback_query_handler(func=lambda call: True)
def get_callback_data(call):
    global text
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    if call.data == "fl":
        text = f"Выберите тариф:"
        btn_1 = types.KeyboardButton("Обычный")
        btn_2 = types.KeyboardButton("Высокогорник")
        markup.add(btn_1, btn_2)
    if call.data == "ul":
        text = f"Выберите тариф"
        btn_1 = types.KeyboardButton("Небытовой")
        btn_2 = types.KeyboardButton("Насос, религиия, троллейбус")
        btn_3 = types.KeyboardButton("Злоторудный")
        btn_4 = types.KeyboardButton("Цемзавод")
        markup.add(btn_1, btn_2, btn_3, btn_4)

    bot.send_message(call.message.chat.id, text, reply_markup=markup)


bot.polling()
