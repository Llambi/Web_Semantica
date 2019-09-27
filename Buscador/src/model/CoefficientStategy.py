from abc import ABC

from src.model.BagOfWords import BagOfWords


class CoefficientStrategy(ABC):

    def exec(self):
        pass


class DiceStrategy(CoefficientStrategy):
    def __init__(self, bag1: BagOfWords, bag2: BagOfWords):
        self.__bag1 = bag1
        self.__bag2 = bag2

    def exec(self):
        return 2.0 * len(self.__bag1.intersection(self.__bag2)) / (len(self.__bag1) + len(self.__bag2))


class JaccardStrategy(CoefficientStrategy):
    def __init__(self, bag1: BagOfWords, bag2: BagOfWords):
        self.__bag1 = bag1
        self.__bag2 = bag2

    def exec(self):
        return len(self.__bag1.intersection(self.__bag2)) / len(self.__bag1.union(self.__bag2))


class CosineStrategy(CoefficientStrategy):
    def __init__(self, bag1: BagOfWords, bag2: BagOfWords):
        self.__bag1 = bag1
        self.__bag2 = bag2

    def exec(self):
        return len(self.__bag1.intersection(self.__bag2)) / (len(self.__bag1) * len(self.__bag2))


class OverlappingStrategy(CoefficientStrategy):
    def __init__(self, bag1: BagOfWords, bag2: BagOfWords):
        self.__bag1 = bag1
        self.__bag2 = bag2

    def exec(self):
        return len(self.__bag1.intersection(self.__bag2)) / min(len(self.__bag1), len(self.__bag2))
