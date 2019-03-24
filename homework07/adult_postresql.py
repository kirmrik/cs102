import psycopg2
from pprint import pprint as pp
from tabulate import tabulate

conn = psycopg2.connect("host=localhost port=5432 dbname=adult user=postgres password=secret")
cursor = conn.cursor() # cursor_factory=psycopg2.extras.DictCursor)

def fetch_all(cursor):
    colnames = [desc[0] for desc in cursor.description]
    records = cursor.fetchall()
    return [{colname:value for colname, value in zip(colnames, record)} for record in records]


print('Посмотрим на первые 5 строк:')
cursor.execute("SELECT * FROM adult LIMIT 5")
records = cursor.fetchall()
print(records, "\n")


print('1. Сколько мужчин и женщин (признак sex) представлено в этом наборе данных?')
cursor.execute(
    """
    SELECT sex, COUNT(*)
        FROM adult
        GROUP BY sex
    """
)
print(tabulate(fetch_all(cursor), "keys", "psql"), "\n")


print('2. Каков средний возраст (признак age) женщин?')
cursor.execute(
    """
    SELECT AVG(age)
        FROM adult WHERE sex = ' Female'
    """
)
print(tabulate(fetch_all(cursor), "keys", "psql"), "\n")


print('3. Какова доля граждан Германии (признак native-country)?')
cursor.execute(
    """
    SELECT native_country, ROUND((COUNT(*) / (SELECT COUNT(*) FROM adult)::numeric), 6)
        FROM adult  WHERE native_country = ' Germany'
        GROUP BY native_country
    """
)
print(tabulate(fetch_all(cursor), "keys", "psql"), "\n")


print('4-5. Каковы средние значения и среднеквадратичные отклонения возраста тех,\n',
      'кто получает более 50K в год (признак salary) и тех,\n',
      'кто получает менее 50K в год?')
cursor.execute(
    """
    SELECT salary,
            AVG(age), STDDEV(age)
        FROM adult
        GROUP BY salary
    """
)
print(tabulate(fetch_all(cursor), "keys", "psql"), "\n")


print('6. Правда ли, что люди, которые получают больше 50k,\n',
      'имеют как минимум высшее образование? (признак education –\n',
      'Bachelors, Prof-school, Assoc-acdm, Assoc-voc, Masters или Doctorate)')
cursor.execute(
    """
    SELECT education, COUNT(*) as " >50K"
        FROM adult WHERE salary = ' >50K' 
        GROUP BY education
        ORDER BY COUNT(*) DESC
    """
)
print(tabulate(fetch_all(cursor), "keys", "psql"), "\n", "Неправда", "\n")


print('7. Выведите статистику возраста для каждой расы (признак race) и каждого пола.\n',
      'Используйте groupby и describe. Найдите таким\n',
      'образом максимальный возраст мужчин расы Amer-Indian-Eskimo.')
cursor.execute(
    """
    SELECT sex, race,
            AVG(age), STDDEV(age), MIN(age),
            PERCENTILE_DISC(0.5) WITHIN GROUP (ORDER BY age) as "50%", MAX(age)
        FROM adult
        GROUP BY sex, race
        ORDER BY sex, race
    """
)
print(tabulate(fetch_all(cursor), "keys", "psql"), "\n", "82", "\n")


print('8. Среди кого больше доля зарабатывающих много (>50K):\n',
      'среди женатых или холостых мужчин (признак marital-status)?\n',
      'Женатыми считаем тех, у кого marital-status начинается с Married\n',
      '(Married-civ-spouse, Married-spouse-absent или Married-AF-spouse),\n'
      'остальных считаем холостыми.')
cursor.execute(
    """
    SELECT ROUND((COUNT(*) / (SELECT COUNT(*) FROM adult)::numeric), 6) as "Married"
        FROM adult
        WHERE marital_status LIKE ' Mar%' AND salary = ' >50K'
    """
)
print(tabulate(fetch_all(cursor), "keys", "psql"), "\n")
cursor.execute(
    """
    SELECT ROUND((COUNT(*) / (SELECT COUNT(*) FROM adult)::numeric), 6) as "Unarried"
        FROM adult
        WHERE marital_status LIKE '%d' AND salary = ' >50K'
    """
)
print(tabulate(fetch_all(cursor), "keys", "psql"), "\n")


print('9. Какое максимальное число часов человек работает в неделю\n'
      '(признак hours-per-week)? Сколько людей работают такое количество\n'
      'часов и каков среди них процент зарабатывающих много?')
cursor.execute(
    """
    SELECT MAX(hours_per_week), COUNT(*)
        FROM adult
        WHERE hours_per_week = (SELECT MAX(hours_per_week) FROM adult)
    """
)
print(tabulate(fetch_all(cursor), "keys", "psql"), "\n")
cursor.execute(
    """
    SELECT salary, ROUND((COUNT(*) / (SELECT COUNT(*) FROM adult WHERE hours_per_week = (SELECT MAX(hours_per_week) FROM adult))::numeric), 4) * 100 as "%"
        FROM adult
        WHERE hours_per_week = (SELECT MAX(hours_per_week) FROM adult)
        GROUP BY salary
    """
)
print(tabulate(fetch_all(cursor), "keys", "psql"), "\n")


print('10. Посчитайте среднее время работы (hours-per-week) зарабатывающих\n',
      'мало и много (salary) для каждой страны (native-country).')
cursor.execute(
    """
    SELECT native_country, salary, ROUND(AVG(hours_per_week), 0) as "average hours per week"
        FROM adult
        GROUP BY native_country, salary
        ORDER BY native_country, salary
        LIMIT 10 OFFSET 43
    """
)
print(tabulate(fetch_all(cursor), "keys", "psql"), "\n")
