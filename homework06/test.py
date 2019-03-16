import csv
from bayes import NaiveBayesClassifier
from db import News, session

# test_SMSSpamCollection
with open("data\SMSSpamCollection", encoding='utf-8') as f:
    data = list(csv.reader(f, delimiter="\t"))
X, y = [], []
for target, msg in data:
    X.append(msg)
    y.append(target)
X_train, y_train, X_test, y_test = X[:3900], y[:3900], X[3900:], y[3900:]
model = NaiveBayesClassifier()
model.fit(X_train, y_train)
print(model.score(X_test, y_test))

# test_news.db
s = session()
rows = s.query(News).filter(News.label != None).all()
labels = [row.label for row in rows]
titles = [row.title + ' ' + row.author + ' ' + row.url.split('//')[-1].split('/')[0].replace('.', '') for row in rows]
model = NaiveBayesClassifier()
model.fit(titles, labels)
print(model.score(titles, labels))
