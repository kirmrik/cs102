df <- read.csv("adult.data.csv")
str(df)
print('1')
table(df$sex)
print('2')
mean(df$age[df$sex == ' Female'])
print('3')
prop.table(table(df$native.country))[c(' Germany')]
print('4-5')
library(dplyr)
df %>% group_by(salary) %>%
  summarise(mean = mean(age),
            std = sd(age))
print('6')
table(df$education, df$salary)[,c(' >50K')]
print('7')
df %>% group_by(sex, race) %>%
  summarise(mean = mean(age),
            std = sd(age),
            min = min(age),
            median = median(age),
            max = max(age))
print('8')
print('Married')
sum(prop.table(table(df$sex, df$marital.status, df$salary))[
  c(' Male'),
  c(' Married-AF-spouse', ' Married-civ-spouse', ' Married-spouse-absent'),
  c(' >50K')])
print('Unmarried')
sum(prop.table(table(df$sex, df$marital.status, df$salary))[
  c(' Male'),
  c(' Divorced', ' Never-married', ' Separated', ' Widowed'),
  c(' >50K')])
print('9')
table(df$hours.per.week)[c(as.character(max(df$hours.per.week)))]
prop.table(table(df$salary[df$hours.per.week == as.character(max(df$hours.per.week))]))
print('10')
tail(df %>% group_by(native.country, salary) %>%
  summarise(mean = round(mean(hours.per.week))), 39)