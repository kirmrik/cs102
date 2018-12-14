import datetime as dt
from statistics import median
from typing import Optional

from api import get_friends
from api_models import User


def age_from_bdate(bd: str) -> Optional[float]:
    """ Вычисляет возраст по дате рождения
    :param bdate: дата рождения в виде "dd.mm.yyyy"
    """
    now = dt.datetime.now()
    then = dt.datetime(int(bd.split(".")[2]),
                        int(bd.split(".")[1]),
                        int(bd.split(".")[0])
                        )
    delta = now - then
    return round(delta.days/365, 2)


def age_predict(user_id: int) -> Optional[float]:
    """ Наивный прогноз возраста по возрасту друзей
    Возраст считается как медиана среди возраста всех друзей пользователя
    :param user_id: идентификатор пользователя
    :return: медианный возраст пользователя
    """
    assert isinstance(user_id, int), "user_id must be positive integer"
    assert user_id > 0, "user_id must be positive integer"
    dates = get_friends(user_id, 'bdate')
    ages = []
    for i in range(dates['response']['count']):
        try:
            if(len(dates['response']['items'][i]['bdate']) > 5):
                ages.append(age_from_bdate(dates['response']['items'][i]['bdate']))
        except:
            pass
    return round(median(ages), 2)
