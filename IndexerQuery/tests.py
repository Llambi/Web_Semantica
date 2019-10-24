# -*- encoding:utf-8 -*-

# Estos test se ejecutan con el siguiente comando:
#    python -m unittest discover -v
# en la carpeta donde esta este fichero

from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import unittest
from io import StringIO

from model.QueryAnalizer import QueryAnalizer
from model.bag_of_words import BagOfWords
from model.indexer_v1 import Indexer


class TestBagOfWords(unittest.TestCase):
    def test_init_with_str(self):
        """Prueba la inicialización con strings
        """
        self.assertDictEqual(
            BagOfWords("cat dog cow").values, {
                "cat": 1,
                "dog": 1,
                "cow": 1
            })
        self.assertDictEqual(
            BagOfWords(text="Cat dog cat").values, {
                "cat": 2,
                "dog": 1
            })

    def test_init_with_dict(self):
        """Prueba la inicialización con diccinoarios
        """
        self.assertDictEqual(
            BagOfWords(values={
                "cat": 1,
                "dog": 1,
                "cow": 1
            }).values, {
                "cat": 1,
                "dog": 1,
                "cow": 1
            })
        self.assertDictEqual(
            BagOfWords(values={
                "cat": 2,
                "dog": 1
            }).values, {
                "cat": 2,
                "dog": 1
            })

    def test_init_with_symbols_in_str(self):
        """Prueba la inicialización con strings que contengan símbolos de puntuación
        """
        self.assertDictEqual(
            BagOfWords(" cat, dog! cow.").values, {
                "cat": 1,
                "dog": 1,
                "cow": 1
            })
        self.assertDictEqual(
            BagOfWords(text="cat dog?? cat!!! ").values, {
                "cat": 2,
                "dog": 1
            })

    def test_str(self):
        """Prueba la conversión a string
        """
        txt = str(BagOfWords("cat dog cow"))
        self.assertTrue(txt.startswith("{"))
        self.assertIn("'cat': 1", txt)
        self.assertIn("'dog': 1", txt)
        self.assertIn("'cow': 1", txt)
        self.assertTrue(txt.endswith("}"))

    def test_len(self):
        """Prueba el tamaño del vector
        """
        self.assertEqual(len(BagOfWords()), 0)
        self.assertEqual(len(BagOfWords("cat dog cow")), 3)
        self.assertEqual(len(BagOfWords(text="cat dog cat")), 2)

    def test_iter(self):
        """Prueba el iterador
        """
        self.assertSequenceEqual(sorted(iter(BagOfWords())), [])
        self.assertSequenceEqual(
            sorted(iter(BagOfWords("cat cow dog"))), [("cat", 1), ("cow", 1),
                                                      ("dog", 1)])
        self.assertSequenceEqual(
            sorted(iter(BagOfWords(text="cat dog cat"))), [("cat", 2),
                                                           ("dog", 1)])

    def test_intersection(self):
        """Prueba la interesección de dos bag-of-words
        """
        bag1 = BagOfWords("cat dog cow fish cat cat fish")
        bag2 = BagOfWords("dog grape banana peach")
        self.assertDictEqual(bag1.intersection(bag2).values, {"dog": 1})

    def test_union(self):
        """Prueba la union de dos bag-of-words
        """
        bag1 = BagOfWords("cat dog cow fish cat cat fish")
        bag2 = BagOfWords("dog grape banana peach")
        self.assertDictEqual(
            bag1.union(bag2).values, {
                "banana": 1,
                "cat": 3,
                "cow": 1,
                "dog": 2,
                "fish": 2,
                "grape": 1,
                "peach": 1
            })

    def test_document_len(self):
        """Prueba el tamaño del documento, no del vector
        """
        bag1 = BagOfWords("cat dog cow fish cat cat fish")
        bag2 = BagOfWords("dog grape banana peach")
        self.assertEqual(bag1.document_len(), 7)
        self.assertEqual(bag2.document_len(), 4)
        self.assertEqual(bag1.intersection(bag2).document_len(), 1)
        self.assertEqual(bag1.union(bag2).document_len(), 11)


class TestIndexer(unittest.TestCase):
    """
    Esta prueba usa el siguiente ejemplo como modelo
    https://en.wikipedia.org/wiki/Tf%E2%80%93idf#Example_of_tf%E2%80%93idf
    """

    texts = [
        "this is a a sample",
        "this is another another example example example"
    ]

    expected = {"this": {"idf": 1.0, "documents": [{"tf": 0.2, "document": {"this": 1, "is": 1, "a": 2, "sample": 1}},
                                                   {"tf": 0.14285714285714285,
                                                    "document": {"this": 1, "is": 1, "another": 2, "example": 3}}]},
                "is": {"idf": 1.0, "documents": [{"tf": 0.2, "document": {"this": 1, "is": 1, "a": 2, "sample": 1}},
                                                 {"tf": 0.14285714285714285,
                                                  "document": {"this": 1, "is": 1, "another": 2, "example": 3}}]},
                "a": {"idf": 1.3010299956639813,
                      "documents": [{"tf": 0.4, "document": {"this": 1, "is": 1, "a": 2, "sample": 1}}]},
                "sample": {"idf": 1.3010299956639813,
                           "documents": [{"tf": 0.2, "document": {"this": 1, "is": 1, "a": 2, "sample": 1}}]},
                "another": {"idf": 1.3010299956639813, "documents": [
                    {"tf": 0.2857142857142857, "document": {"this": 1, "is": 1, "another": 2, "example": 3}}]},
                "example": {"idf": 1.3010299956639813, "documents": [
                    {"tf": 0.42857142857142855, "document": {"this": 1, "is": 1, "another": 2, "example": 3}}]}}

    def test_index_creation(self):
        """Prueba la creación del indice

        Esta prueba usa el siguiente ejemplo como modelo
        https://en.wikipedia.org/wiki/Tf%E2%80%93idf#Example_of_tf%E2%80%93idf
        """

        self.maxDiff = None

        indexer = Indexer()
        for text in self.texts:
            text = text.strip()
            bag = BagOfWords(text, enable_stemming=False, filter_stopwords=False)
            indexer.index(bag)

        test = self.expected["words_index"].__str__()
        print(test)
        fd = StringIO()
        indexer.dump(fd)
        result = fd.getvalue().replace("\"", "'")
        print(result)

        self.assertEqual(test, result)

    def test_dump(self):
        """Prueba que el fichero JSON generado sea correcto
        """
        indexer = Indexer()
        for text in self.texts:
            text = text.strip()
            bag = BagOfWords(text, enable_stemming=False, filter_stopwords=False)
            indexer.index(bag)
        fd = StringIO()
        indexer.dump(fd)
        print(fd.getvalue())
        fd.seek(0)


class TestQueryAnalizer(unittest.TestCase):
    """
       Esta prueba usa el siguiente ejemplo como modelo
       https://janav.wordpress.com/2013/10/27/tf-idf-and-cosine-similarity/
       """
    expected = {'life': [('The unexamined life is not worth living', 0.10591749249194375),
                         ('The game of life is a game of everlasting learning', 0.07414224474436064)],
                'learning': [('Never stop learning', 0.19653851254695906),
                             ('The game of life is a game of everlasting learning', 0.058961553764087724)]}

    documents = [
        "The game of life is a game of everlasting learning",
        "The unexamined life is not worth living",
        "Never stop learning"
    ]

    query = "life learning"

    def test_cosine_similarity(self):
        analizer = QueryAnalizer(self.query, self.documents, enable_stemming=False, filter_stopwords=False)
        result = analizer.cosine_similarity()
        self.assertDictEqual(self.expected, result)


if __name__ == '__main__':
    unittest.main()
