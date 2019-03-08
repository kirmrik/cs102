import nltk
from nltk.corpus import stopwords
from textblob import TextBlob
from textblob import Word


def clean(text):
    tb_text = TextBlob(text)
    stop_words = nltk.corpus.stopwords.words('english')
    words_list = [word for word in tb_text.words.stem().lower() if word not in stop_words]
    cleaned_text = list(set(words_list))
    return cleaned_text
