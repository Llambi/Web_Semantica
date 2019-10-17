# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

# nltk.download('punkt')
# nltk.download('wordnet')
# nltk.download('stopwords')
from functools import reduce
from json import JSONEncoder

from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer


class MyEncoder(JSONEncoder):
    def default(self, o):
        return o.values


class BagOfWords(object):
    def __init__(self, text=None, values=None, enable_stemming=True, filter_stopwords=True):
        """Constructor

        Si recibe un string mediante el argumento text lo convierte a un
        diccionario. Si recibe un diccionario simplemente lo copia para su
        uso interno.
        """
        self.enable_stemming = enable_stemming
        self.filter_stopwords = filter_stopwords
        self.text = text
        if values is not None:
            self.values = values
        elif type(text) is dict:
            self.values = text
        elif type(text) is str:
            self.values = self.string_to_bag_of_words(text, {})
        elif type(text) is list:
            bag = {}
            for i in text:
                bag = self.string_to_bag_of_words(text, bag)
            self.values = bag
        else:
            self.values = {}

    def __str__(self):
        """Devuelve un string con la representacion del objeto

        El objeto BagOfWords(“A b a”) está representado por el string
        "{‘a’: 2, ‘b’: 1}"
        """
        return str(self.values)

    def __len__(self):
        """Devuelve el tamaño del diccionario"""
        return len(self.values)

    def __iter__(self):
        """Crea un iterador que devuelve la clave y el valor de cada
      elemento del diccionario

        El diccionario {‘a’: 1, ‘b’: 2} devuelve:
        - (‘a’, 1) en la primera llamada
        - (‘b’, 2) en la primera llamada
        """
        for x in self.values.items():
            yield x

    def intersection(self, other):
        """Intersecta 2 bag-of-words

        La intersección de “a b c a” con “a b d” es:
        {‘a’: 1, ‘b’: 1}
        """
        keys_a = set(self.values)
        keys_b = set(other.values)
        intersection = {}
        for word in keys_a & keys_b:
            intersection[word] = min(self.values[word], other.values[word])
        return BagOfWords(values=intersection)

    def union(self, other):
        """Une 2 bag-of-words

        La unión de “a b c a” con “a b d” es:
        {‘a’: 3, ‘b’: 2, ‘c’: 1, ‘d’: 1}
        """
        keys_a = set(self.values)
        keys_b = set(other.values)
        union = {}
        for word in keys_a | keys_b:
            val1 = self.values[word] if word in self.values else 0
            val2 = other.values[word] if word in other.values else 0
            union[word] = val1 + val2
        return BagOfWords(values=union)

    def document_len(self):
        return reduce((lambda x, value: x + value), self.values.values(), 0)

    def string_to_bag_of_words(self, text, bag):
        """Convierte un string a bag of words"""
        lemmatizer = WordNetLemmatizer()
        words = word_tokenize(text)
        # words =  [unicode(x, errors='replace') for x in words]
        stop = set(stopwords.words('english')) if self.filter_stopwords else []
        signosPuntuacion = ["?", "¿", "¡", "!", " ", ",", ".", ";", ":"]
        # Eliminar símbolos de puntuación y palabras vacias
        tokens = list(filter(lambda x: x not in signosPuntuacion and x not in stop, words))

        for word in tokens:
            word = word.lower()  # Pasar a minusculas
            if self.enable_stemming:
                word = lemmatizer.lemmatize(word)  # Lematizar mediante NLTK
            if word in bag:  # Almacenar palabra con el numero de apariciones de la misma
                bag[word] = 1 + bag[word]
            else:
                bag[word] = 1

        return bag
