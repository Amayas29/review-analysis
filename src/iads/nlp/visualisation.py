from sklearn.feature_extraction.text import TfidfVectorizer
from wordcloud import WordCloud
import numpy as np


def get_wordcloud(data, stop_words):
    vectorizer = TfidfVectorizer(
        use_idf=False, stop_words=stop_words, ngram_range=(2, 2))
    vectors = vectorizer.fit_transform(data)

    counts = np.array(vectors.sum(axis=0))[0]

    dico = dict()
    words = vectorizer.get_feature_names_out()

    for i in range(len(words)):
        w = words[i]
        dico[w] = counts[i]

    return WordCloud(background_color='white', stopwords=stop_words, max_words=100).generate_from_frequencies(dico)
