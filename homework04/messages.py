from collections import Counter
import datetime
from typing import List, Tuple
import plotly
import plotly.plotly as py
import plotly.graph_objs as go

from api import messages_get_history
from api_models import Message
import config


Dates = List[datetime.date]
Frequencies = List[int]


plotly.tools.set_credentials_file(
    username=config.PLOTLY_CONFIG['username'],
    api_key=config.PLOTLY_CONFIG['api_key']
)


def fromtimestamp(ts: int) -> datetime.date:
    return datetime.datetime.fromtimestamp(ts).date()


def count_dates_from_messages(messages: List[Message]) -> Tuple[Dates, Frequencies]:
    """ Получить список дат и их частот
    :param messages: список сообщений
    """
    dates = []
    x = []
    y = []
    for value in messages:
        dates.append(fromtimestamp(value.get('date')))
    date_counter = Counter(dates)
    for key, value in date_counter.items():
        x.append(key)
        y.append(value)
    return x, y


def plotly_messages_freq(dates: Dates, freq: Frequencies) -> None:
    """ Построение графика с помощью Plot.ly
    :param date: список дат
    :param freq: число сообщений в соответствующую дату
    """
    data = [go.Scatter(x=dates, y=freq)]
    py.plot(data)
