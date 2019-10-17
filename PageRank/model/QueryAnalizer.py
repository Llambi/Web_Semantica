class QueryAnalizer:
    def __init__(self, query=None, indexer=None):
        self.__query = query
        self.__indexer = indexer

    def cosine_similarity(self):
        map(lambda word: self.__indexer.score(word), self.__query.strip().split(" "))
