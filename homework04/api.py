import requests
import time
import datetime as dt
from typing import Any
import config


def get(url: str, params: dict = {}, timeout: int = 5, max_retries: int = 5,
        backoff_factor: float = 0.3) -> requests.models.Response:
    """ Выполнить GET-запрос
    :param url: адрес, на который необходимо выполнить запрос
    :param params: параметры запроса
    :param timeout: максимальное время ожидания ответа от сервера
    :param max_retries: максимальное число повторных запросов
    :param backoff_factor: коэффициент экспоненциального нарастания задержки
    """
    for i in range(max_retries):
        try:
            response = requests.get(url, params)
            response.raise_for_status()
            if response.json().get('error'):
                print(response.json()['error']['error_msg'])
                raise SystemExit()
            return response
        except requests.ReadTimeout as errt:
            if i == max_retries - 1:
                print("ReadTimeout:", errt)
                continue
            pause = (2 ** i) * backoff_factor
            time.sleep(pause)
        except requests.exceptions.HTTPError as errh:
            if i == max_retries - 1:
                print("HTTPError:", errh)
                continue
            pause = (2 ** i) * backoff_factor
            time.sleep(pause)
        except requests.exceptions.ConnectionError as errc:
            if i == max_retries - 1:
                print("ConnectionError:", errc)
                continue
            pause = (2 ** i) * backoff_factor
            time.sleep(pause)
        except requests.exceptions.RequestException as err:
            if i == max_retries - 1:
                print("Error:", err)
                continue
            pause = (2 ** i) * backoff_factor
            time.sleep(pause)


def get_friends(user_id: int, fields: str = '') -> Any:
    """ Вернуть данные о друзьях пользователя
    :param user_id: идентификатор пользователя, список друзей которого нужно получить
    :param fields: список полей, которые нужно получить для каждого пользователя
    """
    assert isinstance(user_id, int), "user_id must be positive integer"
    assert isinstance(fields, str), "fields must be string"
    assert user_id > 0, "user_id must be positive integer"
    query_params = {
        'access_token': config.VK_CONFIG.get('access_token'),
        'user_id': user_id,
        'fields': fields,
        'v': config.VK_CONFIG.get('version')
    }
    url = "{}/friends.get".format(config.VK_CONFIG.get('domain'))
    friends = get(url, query_params)
    time.sleep(0.333334)
    return friends.json()


def messages_get_history(user_id: int, offset: int = 0, count: int = 20) -> Any:
    """ Получить историю переписки с указанным пользователем
    :param user_id: идентификатор пользователя, с которым нужно получить историю переписки
    :param offset: смещение в истории переписки
    :param count: число сообщений, которое нужно получить
    """
    assert isinstance(user_id, int), "user_id must be positive integer"
    assert user_id > 0, "user_id must be positive integer"
    assert isinstance(offset, int), "offset must be positive integer"
    assert offset >= 0, "user_id must be positive integer"
    assert count >= 0, "user_id must be positive integer"
    limit = 200
    url = "{}/messages.getHistory".format(config.VK_CONFIG.get('domain'))
    query_params = {
        'access_token': config.VK_CONFIG.get('access_token'),
        'user_id': user_id,
        'offset': offset,
        'count': min(limit, count),
        'v': config.VK_CONFIG.get('version')
    }
    messages = []
    history = get(url, query_params)
    count = min(history.json()['response']['count'] - offset, count)
    messages += history.json()['response']['items']
    count -= min(limit, count)
    while count > 0:
        begin = dt.datetime.now()
        query_params['offset'] += 200
        query_params['count'] = min(limit, count)
        history = get(url, query_params)
        messages += history.json()['response']['items']
        count -= min(limit, count)
        end = dt.datetime.now()
        time.sleep(max(0, 0.333334 - (end - begin).total_seconds()))
    return messages

def get_last_name(user_id: int) -> str:
    """ Вернуть имя пользователя
    :param user_id: идентификатор пользователя, фамилию которого нужно получить
    """
    assert isinstance(user_id, int), "user_id must be positive integer"
    assert user_id > 0, "user_id must be positive integer"
    query_params = {
        'access_token': config.VK_CONFIG.get('access_token'),
        'user_id': user_id,
        'v': config.VK_CONFIG.get('version')
    }
    url = "{}/users.get".format(config.VK_CONFIG.get('domain'))
    user = get(url, query_params)
    return user.json()['response'][0].get('last_name')
