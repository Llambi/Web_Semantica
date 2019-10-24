import numpy as np

from model.indexer_v1 import Indexer


class QueryAnalizer:
    def __init__(self, query, document_list, enable_stemming=True, filter_stopwords=True):
        self.__query = Indexer([query], enable_stemming=enable_stemming, filter_stopwords=filter_stopwords)
        self.__indexer = Indexer(document_list, enable_stemming=enable_stemming, filter_stopwords=filter_stopwords)
        self.result = None

    def cosine_similarity(self):
        if self.result is not None:
            return self.result

        result = {}
        for query_term, value in self.__query.words_index.items():
            indexer_term = self.__indexer.words_index[query_term]

            tf_idf_query_term = self.__query.words_index[query_term]["idf"] * \
                                self.__query.words_index[query_term]["documents"][0]["tf"]

            tf_documents = list(map(lambda doc: doc["tf"], indexer_term["documents"]))

            dot_product = np.dot(tf_idf_query_term, tf_documents)

            result[query_term] = list(zip(
                list(
                    map(
                        lambda doc: doc["document"].text,
                        indexer_term["documents"]))
                ,
                list(
                    map(
                        lambda elem: elem / (np.linalg.norm(tf_idf_query_term) + np.linalg.norm(tf_documents)),
                        dot_product
                    ))
            ))
        self.result = result
        for key, elm in self.result.items():
            self.result[key] = sorted(elm, key=lambda tup: tup[1], reverse=True)
        return self.result
