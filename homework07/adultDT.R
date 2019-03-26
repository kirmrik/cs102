library(data.table)
dft <- fread('adult.data.csv')
str(dft)
# 1 Сколько мужчин и женщин (признак sex) представлено в этом наборе данных?
table(dft$sex)
# 2 Каков средний возраст (признак age) женщин?
dft[sex == 'Female', mean(age)]
# 3 Какова доля граждан Германии (признак native-country)?
dft[`native-country` == 'Germany', .N] / nrow(dft)
# 4-5 Каковы средние значения и среднеквадратичные отклонения возраста тех,
# кто получает более 50K в год (признак salary) и тех, кто получает менее 50K в год?
dft[,.(mean = mean(age), std = sd(age)), by = salary]
# 6 Правда ли, что люди, которые получают больше 50k, имеют как минимум высшее образование?
# (признак education Bachelors, Prof-school, Assoc-acdm, Assoc-voc, Masters или Doctorate)
dft[salary == '>50K', .N, by = education][order(-N)]
# 7 Выведите статистику возраста для каждой расы (признак race) и каждого пола.
dft[,.(mean = mean(age),
       std = sd(age),
       min = min(age),
       median = median(age),
       max = max(age)), by = .(sex, race)][order(sex, race)]
# 8 Среди женатых или холостых мужчин больше доля зарабатывающих много (>50K)?
print('Married')
dft[`marital-status` %in% list('Married-AF-spouse',
                               'Married-civ-spouse',
                               'Married-spouse-absent') & salary == '>50K' & sex == 'Male', .N] / nrow(dft)
print('Unmarried')
dft[`marital-status` %in% list('Divorced',
                               'Never-married',
                               'Separated',
                               'Widowed') & salary == '>50K' & sex == 'Male', .N] / nrow(dft)
# 9 Какое максимальное число часов человек работает в неделю (признак hours-per-week)?
# Сколько людей работают такое количество часов и каков среди них процент зарабатывающих много?
dft[`hours-per-week` == max(`hours-per-week`), .(count = .N), by = .(max_hours_per_week = `hours-per-week`)]
total = nrow(dft[`hours-per-week` == max(`hours-per-week`)])
dft[`hours-per-week` == max(`hours-per-week`), .(pers = round(.N / total * 100, 1)), by = salary]
# 10 Посчитайте среднее время работы (hours-per-week) зарабатывающих
# мало и много (salary) для каждой страны (native-country).
dft[, .(mean = round(mean(`hours-per-week`))), by = .(`native-country`, salary)][order(`native-country`, salary)]
