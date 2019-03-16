import datetime as dt
from statistics import median
from typing import Optional

from api import get_friends


def age_from_bdate(bd: str) -> int:
    """ Вычисляет возраст по дате рождения
    :param bdate: дата рождения в виде "dd.mm.yyyy"
    """
    today = dt.datetime.now()
    born = dt.datetime(int(bd.split(".")[2]),
                       int(bd.split(".")[1]),
                       int(bd.split(".")[0])
                       )
    try:
        birthday = born.replace(year=today.year)
    except ValueError:  # February 29
        birthday = born.replace(year=today.year, month=born.month+1, day=1)
    if birthday > today:
        return today.year - born.year - 1
    return today.year - born.year


def age_predict(user_id: int) -> Optional[float]:
    """ Наивный прогноз возраста по возрасту друзей
    Возраст считается как медиана среди возраста всех друзей пользователя
    :param user_id: идентификатор пользователя
    :return: медианный возраст пользователя
    """
    assert isinstance(user_id, int), "user_id must be positive integer"
    assert user_id > 0, "user_id must be positive integer"
    friends = get_friends(user_id, 'bdate')
    ages = []
    if friends:
        for friend in friends:
            try:
                if len(friend.get('bdate')) > 5:
                    ages.append(age_from_bdate(friend.get('bdate')))
            except:
                pass
    else:
        return None
    if ages:
        return median(ages)
    return None
