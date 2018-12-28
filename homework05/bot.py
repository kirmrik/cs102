from typing import Any
import datetime as dt
import telebot
import requests
from bs4 import BeautifulSoup
import config


access_token = config.BOT_CONFIG.get('access_token')
domain = config.BOT_CONFIG.get('domain')

bot = telebot.TeleBot(access_token)


@bot.message_handler(commands=['help', '?'])
def helper(message):
    """Сверить дату и время, вывести список команд"""
    now = 'Сверим дату и время:' + (dt.datetime.today() + dt.timedelta(hours=3)).strftime('%Y-%m-%d %H:%M')
    bot.send_message(message.chat.id, now, parse_mode='HTML')
    resp = """
    <b>Команды бота:</b>
<b>1.</b> /weekday [week] Group_number - <i>расписание для группы на указанный день</i>
<b>2.</b> /near Group_number - <i>ближайшее занятие для группы</i>
<b>3.</b> /tomorrow Group_number - <i>расписание для группы на следующий учебный день</i>
<b>4.</b> /all [week] Group_number - <i>расписание для группы на неделю</i>
В квадратных скобках необязательный параметр"""
    bot.send_message(message.chat.id, resp, parse_mode='HTML')


def get_page(group: str, week: Any = '') -> str:
    """Получить страницу с расписанием"""
    if week:
        week = str(week) + '/'
    url = '{domain}/{group}/{week}/raspisanie_zanyatiy_{group}.htm'.format(
        domain=config.BOT_CONFIG.get('domain'),
        week=week,
        group=group)
    response = requests.get(url)
    web_page = response.text
    return web_page


def parse_schedule(web_page: str, day: str) -> Any:
    """Получить списки времени, адресов, аудиторий и названий дисциплин"""
    soup = BeautifulSoup(web_page, "html5lib")

    # Проверяем наличие расписания
    check = soup.find("article", attrs={"class": "content_block"})
    check = soup.find("article", attrs={"class": "content_block"})
    check = check.text
    if 'Расписание не найдено' in check:
        return None

    # Получаем таблицу с расписанием на нужный день
    schedule_table = soup.find("table", attrs={"id": day})

    # Время проведения занятий
    times_list = schedule_table.find_all("td", attrs={"class": "time"})
    times_list = [time.span.text for time in times_list]

    # Место проведения занятий
    locations_list = schedule_table.find_all("td", attrs={"class": "room"})
    room_list = [room.dd.text for room in locations_list]  # номер аудитории
    locations_list = [room.span.text for room in locations_list]

    # Название дисциплин и имена преподавателей
    lessons_list = schedule_table.find_all("td", attrs={"class": "lesson"})
    lessons_list = [lesson.dl.text for lesson in lessons_list]
    lessons_list = [' '.join(lesson.split()) for lesson in lessons_list]
    # persons_list = [lesson.dt.text for lesson in lessons_list]
    # lessons_list = [lesson.dd.text for lesson in lessons_list]
    return times_list, locations_list, room_list, lessons_list


@bot.message_handler(commands=['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday'])
def get_schedule(message):
    """ Получить расписание на указанный день """
    num_day = {
        "/monday": "1day",
        "/tuesday": "2day",
        "/wednesday": "3day",
        "/thursday": "4day",
        "/friday": "5day",
        "/saturday": "6day"
    }
    try:
        day, week, group = message.text.split()
        web_page = get_page(group, week)
    except ValueError:
        try:
            day, group = message.text.split()
            web_page = get_page(group)
        except ValueError:
            bot.send_message(message.chat.id, 'Неправильный формат. Нужно: /weekday [week] Group_number')
            return None
    day = num_day.get(day)
    try:
        times_lst, locations_lst, room_lst, lessons_lst = \
                   parse_schedule(web_page, day)
        resp = ''
        for time, location, room, lesson in zip(times_lst, locations_lst, room_lst, lessons_lst):
            resp += '<b>{}</b>\n {}\n <b>{}</b>\n {}\n'.format(time, location, room, lesson)
    except AttributeError:
        resp = 'В этот день у этой группы нет занятий'
    except TypeError:
        resp = 'Расписание не найдено. Проверьте номер группы'
    bot.send_message(message.chat.id, resp, parse_mode='HTML')


@bot.message_handler(commands=['tomorrow'])
def get_tomorrow(message):
    """ Получить расписание на следующий день """
    day = (dt.datetime.today() + dt.timedelta(hours=3)).isoweekday() + 1
    week = 1 + (dt.datetime.today() + dt.timedelta(hours=3)).isocalendar()[1] % 2
    if day == 7:
        day = 1
        week = 1 + ((dt.datetime.today() + dt.timedelta(hours=3)).isocalendar()[1] + 1) % 2
        bot.send_message(message.chat.id, 'Завтра воскресенье - отдыхайте. На всякий случай расписание на понедельник:')
    try:
        _, group = message.text.split()
        web_page = get_page(group, week)
    except ValueError:
        bot.send_message(message.chat.id, 'Неправильный формат. Нужно: /tomorrow Group_number')
        return None
    day = str(day) + 'day'
    try:
        times_lst, locations_lst, room_lst, lessons_lst = \
                   parse_schedule(web_page, day)
        resp = ''
        for time, location, room, lesson in zip(times_lst, locations_lst, room_lst, lessons_lst):
            resp += '<b>{}</b>\n {}\n <b>{}</b>\n {}\n'.format(time, location, room, lesson)
    except AttributeError:
        resp = 'В этот день у этой группы нет занятий'
    except TypeError:
        resp = 'Расписание не найдено. Проверьте номер группы'
    bot.send_message(message.chat.id, resp, parse_mode='HTML')


@bot.message_handler(commands=['all'])
def get_all_schedule(message):
    """ Получить расписание на всю неделю для указанной группы """
    week_day = {
        1: "        Понедельник",
        2: "        Вторник ",
        3: "        Среда ",
        4: "        Четверг ",
        5: "        Пятница ",
        6: "        Суббота ",
        }
    try:
        _, week, group = message.text.split()
        web_page = get_page(group, week)
    except ValueError:
        try:
            _, group = message.text.split()
            web_page = get_page(group)
        except ValueError:
            bot.send_message(message.chat.id, 'Неправильный формат. Нужно: /all [week] Group_number')
            return None
    resp = ''
    for i in range(1, 7):
        day = str(i) + 'day'
        resp += '<b>{}</b>\n'.format(week_day[i])
        try:
            times_lst, locations_lst, room_lst, lessons_lst = \
                       parse_schedule(web_page, day)
            for time, location, room, lesson in zip(times_lst, locations_lst, room_lst, lessons_lst):
                resp += '<b>{}</b>\n {}\n <b>{}</b>\n {}\n'.format(time, location, room, lesson)
        except AttributeError:
            resp += 'В этот день занятий нет\n'
        except TypeError:
            resp = 'Расписание не найдено. Проверьте номер группы'
            bot.send_message(message.chat.id, resp, parse_mode='HTML')
            return None
    bot.send_message(message.chat.id, resp, parse_mode='HTML')


@bot.message_handler(commands=['near'])
def get_near_lesson(message):
    """ Получить ближайшее занятие """
    day_num = {
        "1day": "понедельник",
        "2day": "вторник",
        "3day": "среда",
        "4day": "четверг",
        "5day": "пятница",
        "6day": "суббота",
    }
    time_now = (dt.datetime.now() + dt.timedelta(hours=3)).strftime('%H:%M')
    time_now = int(time_now.replace(':', ''))
    day_now = (dt.datetime.today() + dt.timedelta(hours=3)).isoweekday()
    week = 1 + (dt.datetime.today() + dt.timedelta(hours=3)).isocalendar()[1] % 2
    resp = ''
    if day_now == 7:
        day_now = 1
        week = 1 + ((dt.datetime.today() + dt.timedelta(hours=3)).isocalendar()[1] + 1) % 2
    try:
        _, group = message.text.split()
        web_page = get_page(group, week)
    except ValueError:
        bot.send_message(message.chat.id, 'Неправильный формат. Нужно: /near Group_number')
        return None
    day = str(day_now) + 'day'
    try:
        times_lst, locations_lst, room_lst, lessons_lst = \
                    parse_schedule(web_page, day)
        check = 0
        for i, time in enumerate(times_lst):
            beg, end = time.split('-')
            beg = int(beg.replace(':', ''))
            end = int(end.replace(':', ''))
            if time_now < end:
                check = i + 1
                break
        if check:
            resp += 'Ближайшее занятие сегодня\n<b>{}</b>\n{}\n<b>{}</b>\n{}\n'.format(
                times_lst[check - 1],
                locations_lst[check - 1],
                room_lst[check - 1],
                lessons_lst[check - 1]
                )
            bot.send_message(message.chat.id, resp, parse_mode='HTML')
            return None
    except AttributeError:
        pass
    except TypeError:
        resp = 'Расписание не найдено. Проверьте номер группы'
        bot.send_message(message.chat.id, resp, parse_mode='HTML')
        return None
    while not resp:
        day_now += 1
        if day_now == 7:
            day_now = 1
            week = 1 + ((dt.datetime.today() + dt.timedelta(hours=3)).isocalendar()[1] + 1) % 2
        day = str(day_now) + 'day'
        web_page = get_page(group, week)
        try:
            times_lst, locations_lst, room_lst, lessons_lst = \
                        parse_schedule(web_page, day)
            resp = 'Ближайшее занятие:\n{}\n<b>{}</b>\n{}\n<b>{}</b>\n{}\n'.format(
                day_num.get(day),
                times_lst[0],
                locations_lst[0],
                room_lst[0],
                lessons_lst[0]
                )
            bot.send_message(message.chat.id, resp, parse_mode='HTML')
        except AttributeError:
            check += 1
        if check > 12:
            resp = 'Расслабтесь, ближайшее занятие нескоро.'
            bot.send_message(message.chat.id, resp, parse_mode='HTML')
            break


@bot.message_handler(content_types=['text'])
def resp(message):
    """ Ответить пользователю, сверить дату и время, вывести список команд"""
    bot.send_message(message.chat.id, 'Я бы с удовольствием поболтал с Вами, но мне разрешено только выполнять команды')
    now = 'Сверим дату и время:' + (dt.datetime.today() + dt.timedelta(hours=3)).strftime('%Y-%m-%d %H:%M')
    bot.send_message(message.chat.id, now, parse_mode='HTML')
    resp = """
    <b>Команды бота:</b>
<b>1.</b> /weekday [week] Group_number - <i>расписание для группы на указанный день</i>
<b>2.</b> /near Group_number - <i>ближайшее занятие для группы</i>
<b>3.</b> /tomorrow Group_number - <i>расписание для группы на следующий учебный день</i>
<b>4.</b> /all [week] Group_number - <i>расписание для группы на неделю</i>
В квадратных скобках необязательный параметр"""
    bot.send_message(message.chat.id, resp, parse_mode='HTML')


if __name__ == '__main__':
    bot.polling(True)
