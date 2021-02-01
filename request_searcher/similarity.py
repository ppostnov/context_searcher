import json
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import euclidean_distances


class TextComparor(object):
    """
    """

    def __init__(self, source, candidate):
        self.source = source
        self.candidate = candidate

    def build_corpus(self):
        if len(self.candidate) != 0:
            corpus = [self.source, self.candidate]
        else:
            corpus = [self.source, "Сервисная строка"]
        return corpus

    def build_features(self, corpus):
        vectorizer = CountVectorizer()
        features = vectorizer.fit_transform(corpus).todense()
        return features

    def similarity(self):
        corpus = self.build_corpus()
        features = self.build_features(corpus)
        result = euclidean_distances(features[0], features[1])
        return result[0][0]

    def get_statistic(self):
        sim = self.similarity()
        statistic = {
            "Source": (f"{self.source}"),
            "Candidate": f"{self.candidate}",
            "Difference score": float(sim)
        }
        return float(sim)
