from __future__ import annotations

import argparse
import os
from typing import Optional

from src.model.BagOfWords import BagOfWords


class ConfigMeta(type):
    _instance: Optional[Config] = None

    def __call__(self) -> Config:
        if self._instance is None:
            self._instance = super().__call__()
        return self._instance


class Config(metaclass=ConfigMeta):
    __queries = None
    __texts = None

    def __init__(self):
        args = self.__parse_args()
        self.__queries = self.__process_file(args.queries)
        self.__texts = self.__process_file(args.file)
        self.__output = args.output

    def get_output(self):
        return self.__output

    def get_texts(self):
        return self.__texts

    def get_queries(self):
        return self.__queries

    def __process_file(self, file):
        """
        Procesa el fichero y devuelve una BagOfWords
        """
        try:
            with open(file, 'rb') as file_handler:
                texts = []
                for line in self.__load_lines(file_handler):
                    texts.append(BagOfWords(line.decode("utf-8")))
                return texts
        except (IOError, OSError):
            print("Error opening / processing file")
            print(file)
            return None

    def __load_lines(self, file):
        """
        Metodo generador para leer un archivo largo de forma lazy
        """
        while True:
            data = file.readline()
            if not data:
                break
            yield data

    def __parse_args(self):
        """Parse_args
        Funcion que parsea los argumentos de consola
        """
        parser = argparse.ArgumentParser(description='WebCrawler')
        cwd = os.getcwd()
        parser.add_argument("--file", help="Starting point. Default point:" + cwd + "resources/cran-1400.txt", type=str,
                            default=cwd + "/" + "resources/cran-1400.txt")
        parser.add_argument("--output", help="Ouput point. Default point:" + cwd + "resources/result.txt", type=str,
                            default=cwd + "/" + "resources/result.txt")
        parser.add_argument("--queries", help="Queries file. Default point:" + cwd + "resources/cran-queries.txt",
                            type=str,
                            default=cwd + "/" + "resources/cran-queries.txt")
        args = parser.parse_args()
        return args
