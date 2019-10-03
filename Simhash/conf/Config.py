from __future__ import annotations

import argparse
from typing import Optional



class ConfigMeta(type):
    _instance: Optional[Config] = None

    def __call__(self) -> Config:
        if self._instance is None:
            self._instance = super().__call__()
        return self._instance


class Config(metaclass=ConfigMeta):
    __args = None

    def __init__(self):
        self.__args = self.__parse_args()
        self.__classes = self.__load_class()

    def get_args(self):
        return self.__args

    def get_classes(self):
        return self.__classes

    def __load_class(self):
        python_file = None
        try:
            if self.__args.file.endswith(".py"):
                python_file = self.__args.file[:-3]
            implementation = __import__(python_file)
        except ImportError:
            print("Unable to import: {}".format(python_file))
            return 1
        except AttributeError:
            print("The Python file must define simhash: {}".format(python_file))
            return 1
        return {python_file.split(".")[-1]: implementation}

    def __parse_args(self):
        parser = argparse.ArgumentParser(description='SimHash')
        parser.add_argument("--file", help="Texts file", default="model.Simhash.py")
        parser.add_argument("--output", help="Output file", default="./resources/result.csv")
        parser.add_argument("--truth", help="Truth file", default="./resources/articles_10000.truth", )
        parser.add_argument("--train", help="Truth file", default="./resources/articles_10000.train", )
        parser.add_argument(
            "-r",
            "--restrictiveness",
            type=int,
            default=10,
            help="Use %(default)s hashes")
        parser.add_argument(
            "-l",
            "--lines",
            type=int,
            default=10000,
            help="Lines to parse from file")
        args = parser.parse_args()
        return args
