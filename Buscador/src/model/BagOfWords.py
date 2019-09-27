from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import nltk
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

nltk.download('punkt')
nltk.download('wordnet')
nltk.download('stopwords')


class BagOfWords(object):
    def __init__(self, text=None, values=None):
        """
        Crea un diccionario de tipo Word:str -> Counter:int
        :param text: Si es:
                        - Un string: crea el diccionario.
                        - Un diccionario: Lo copia.
        :param values:
        """
        self.text = text
        if values is not None:
            self.values = values
        elif type(text) is dict:
            self.values = text
        elif type(text) is str:
            self.values = self.__string_to_bag_of_words(text, {})
        elif type(text) is list:
            bag = {}
            for i in text:
                bag = self.__string_to_bag_of_words(text, bag)
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

    def __string_to_bag_of_words(self, text, bag):
        """
        Metodo que dado un texto lo limpia de simbolos de puntuacion y palabras vacias, ademas lematiza las palabras y las
        convierte en minusculas.
        :param text: Texto a tratar.
        :param bag: BagOfWords donde se guardaran las palabras ya tratadas.
        :return: BagOfWords del texto.
        """
        lemmatizer = WordNetLemmatizer()
        words = word_tokenize(text)
        stop_words = set(stopwords.words('english'))
        signos_puntuacion = ["?", "¿", "¡", "!", " ", ",", ".", ";", ":"]
        tokens = list(filter(lambda word: word not in signos_puntuacion and word not in stop_words,
                             words))  # Eliminar símbolos de puntuación

        for token in tokens:
            # if word not in stopWords: # Eliminar palabras vacías
            token = token.lower()  # Pasar a minusculas
            token = lemmatizer.lemmatize(token)  # Lematizar mediante NLTK
            # Almacenar palabra con el numero de apariciones de la misma
            bag[token] = 1 + bag[token] if token in bag else 1
        return bag
