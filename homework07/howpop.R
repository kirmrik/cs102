library(data.table)
dft <- fread('howpop_train.csv')
dft <- dft[,-c(1, 6, 7, 8, 9, 15:17)]
library(lubridate)
dft$year <- year(dft$published)
dft$month <- month(dft$published)
dft$dayofweek <- weekdays(as.Date(dft$published))
dft$hour <- hour(dft$published)
library(ggplot2)
# 1
dt <- tail(dft[, .(value = .N), by = .(year, month)][order(value)], 10)
dt$ym <- paste(as.character(dt$year), as.character(dt$month))
ggplot(dt, aes(x = ym, y = value)) + geom_bar(stat = "identity") # 1
# 2
ggplot(data = dft[(year == 2015) & (month == 3)], aes(x = dayofweek, fill = domain)) + geom_bar(position = "dodge") # 2
# 3
library(ggpubr)
comm.p <- ggplot(dft, aes(x = hour, y = comments, color = domain)) + geom_point()
view.p <- ggplot(dft, aes(x = hour, y = views, color = domain)) + geom_point()
ggarrange(comm.p, view.p, 
          ncol = 1, nrow = 2,
          heights = c(0.5, 0.5)) #3
# 4
dft[is.na(dft)] <- 0
dt <- tail(dft[author != '',.(count = .N,
                              mean = mean(votes_minus)),
               by = author][order(count)], 20)
ggplot(dt, aes(x = author, y = mean)) + geom_bar(stat = "identity") + coord_flip() # 4
# 5
ggplot(data = dft[(dayofweek == 'понедельник') | (dayofweek == 'суббота')], 
       aes(x = hour, fill = dayofweek)) + geom_bar(position = "dodge") # 5

