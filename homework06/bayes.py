from collections import Counter, defaultdict
from math import log
from text import clean


class NaiveBayesClassifier:

    def __init__(self, alpha=1.0):
        self.factor = alpha

    def fit(self, X, y):
        """ Fit Naive Bayes classifier according to X, y. """
        all_words = []
        pairs = []
        classes = defaultdict(lambda: defaultdict(int))
        words = defaultdict(lambda: defaultdict(int))
        self.classes_counter = dict(Counter(y))
        for title, cls in zip(X, y):
            words_list = clean(title)
            for word in words_list:
                all_words.append(word)
                pairs.append((word, cls))
                classes[cls]['appearances'] += 1
        for cls in classes:
            classes[cls]['prior'] = self.classes_counter[cls]/len(y)
        self.classes = classes
        self.words_counter = dict(Counter(all_words))
        self.pairs_counter = dict(Counter(pairs))
        d = len(self.words_counter)
        for word in self.words_counter:
            for cls in classes:
                words[word][cls] = (self.pairs_counter.get((word, cls), 0) + self.factor) / (self.classes[cls]['appearances'] + self.factor * d)
        self.words = words

    def predict(self, X):
        """ Perform classification on an array of test vectors X. """
        classification = []
        for row in X:
            words_list = clean(row)
            P_list = []
            for cls in self.classes:
                ln_P_class = log(self.classes[cls]['prior'])
                for word in words_list:
                    if self.words[word][cls]:
                        ln_P_class += log(self.words[word][cls])
                P_list.append((cls, ln_P_class))
            classification.append(max(P_list, key=lambda x: x[1]))
        return classification

    def score(self, X_test, y_test):
        """ Returns the mean accuracy on the given test data and labels. """
        count = 0
        for record, label in zip(self.predict(X_test), y_test):
            if record[0] == label:
                count += 1
        return count / len(y_test)
