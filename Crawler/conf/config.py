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
    __url_list = None

    def __init__(self):
        self.__args = self.__parse_args()
        self.__url_list = self.__parse_txt(self.__args.file)

    def get_args(self):
        return self.__args

    def get_url_list(self):
        return self.__url_list

    def __parse_txt(self, file):
        return [line.rstrip('\n') for line in open(file)]

    def __parse_args(self):
        """Parse_args
        Funcion que parsea los argumentos de consola
        """
        parser = argparse.ArgumentParser(description='WebCrawler')
        parser.add_argument("--file", help="Starting point. Default point:resources/links.txt", type=str,
                            default="resources/links.txt")
        parser.add_argument("--output", help="End point. Default point:resources/result[Strategy].txt", type=str,
                            default="resources/result.txt")
        parser.add_argument("--sec", help="Number of seconds", type=int, default=2)
        parser.add_argument("--mx", help="The max downloads", type=int, default=10)
        parser.add_argument("--name", help="Crawler´s name", type=str, default="UOCrawler")
        parser.add_argument("-w", help="Type of seed exploration: Width (w)", action="store_true")
        parser.add_argument("-d", help="Type of seed exploration: Depth (d)", action="store_true")
        args = parser.parse_args()
        if args.w and args.d:
            parser.error("-d and -w must not be given together")
        return args
