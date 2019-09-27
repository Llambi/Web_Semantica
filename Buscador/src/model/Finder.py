import operator

from src.model import CoefficientStategy
from src.model.CoefficientStategy import DiceStrategy, JaccardStrategy, CosineStrategy, OverlappingStrategy


class Finder:
    def __init__(self, query, text_bags):
        self.__query = query
        self.__strategies = {
            "DiceStrategy": self.__find_best_text(query, text_bags, DiceStrategy),
            "JaccardStrategy": self.__find_best_text(query, text_bags, JaccardStrategy),
            "CosineStrategy": self.__find_best_text(query, text_bags, CosineStrategy),
            "OverlappingStrategy": self.__find_best_text(query, text_bags, OverlappingStrategy)
        }

    def __find_best_text(self, query, text_bags, strategy: CoefficientStategy):
        values = {}
        for text in text_bags:
            values[text] = strategy(text, query).exec()
        obj = max(values.items(), key=operator.itemgetter(1))
        return obj

    def __str__(self):
        s = '''
            Query: {}
            
                Resultados:
            '''.format(" ".join(self.__query.values.keys()))
        for (k, v) in self.__strategies.items():
            s += '''
                    - Estrategia: {} 
                        · Texto: {}
                        · Mejor resultado: {}
                        · Puntuacion: {}
                        
            '''.format(k, " ".join(v[0].values.keys()), v[0], v[1])
        return s
