import os
import time
from collections import deque
from urllib import robotparser
from urllib.error import HTTPError
from urllib.request import Request, urlopen

from bs4 import BeautifulSoup

from model.ConcretStrategies import DeepStrategy, WidthStrategy


class Crawler:
    """
    Clase Crawler que explora, en profundidad o en anchura, un lista de links dados, y ademas comprueba en el robots si
    puede acceder a los links o no para explorarlos
    """
    __max_urls_per_time = 0
    __sleep_time = 10
    __obtained_urls = None
    __urls = None
    __queue = None
    __strategy = None
    __robot_parser = None

    def __init__(self, urls=None, name="UOCrawler", deep=True, max_urls_per_time=10, sleep_time=5):
        """
        Constructor de la clase Crawler
        :param urls: Lista de urls a explorar, predefinido = lista vacia
        :param name: Nombre del agente Crawler, importante para la comprobacion de Robots, predefinido = UOCrawler
        :param deep: Strategia a seguir para la exploracion, True, en profundidad, False, en anchura
        :param max_urls_per_time: Maximo de url que se exploraran para cada url dada
        :param sleep_time: Tiempo que pasara entre cada request a las urls exploradas
        """
        if urls is None:
            urls = list([])
        self.__robot_parser = robotparser.RobotFileParser()
        self.__urls = urls
        self.__obtained_urls = {}
        self.__queue = deque([])
        self.__crawler_name = name
        if deep:
            self.__strategy = DeepStrategy()
        else:
            self.__strategy = WidthStrategy()
        self.__max_urls_per_time = max_urls_per_time
        self.__sleep_time = sleep_time

    def craw(self):
        """
        Metodo que explora cara url especificada en la lista dada en la creacion del objeto Crawler
        :return: El propio Objeto Crawler
        """
        for url in self.__urls:
            self.__obtained_urls[url] = deque([])
            self.__queue = deque(self.__find_urls(url))
            print("Crawling {}".format(url))
            self.__rec_craw(url, 1)
            self.__queue = deque([])
        return self

    def __rec_craw(self, url, level):
        """
        Metodo que explora, mediante la estrategia indicada en la creacion del Crawler, las urls
        :param url: url a explorar
        :param level: nivel del arbol de exploracion
        """
        if level <= self.__max_urls_per_time:
            new_url = self.__queue.popleft()
            while not self.scanRobots(url, new_url):
                if len(self.__queue) is 0:
                    print("\tEmpty queue for {}".format(url))
                    return
                new_url = self.__queue.popleft()
            self.__obtained_urls[url].append(new_url)
            print("\tCrawling {}".format(new_url))
            self.__strategy.extend(self.__find_urls(new_url), self.__queue)
            self.__rec_craw(url, level + 1)

    def __find_urls(self, origin_url):
        """
        Metodo que crea una lista con las url validas que contiene una dada.
        :param origin_url: Url en la que se buscan las nuevas urls
        :return: Lista con las nuevas urls obtenidas.
        """
        try:
            request = Request(origin_url, headers={"User-Agent": self.__crawler_name, "Accept": "text/html"})
            response = urlopen(request).read()
            time.sleep(self.__sleep_time)
            soup = BeautifulSoup(response.decode("utf-8"), 'html.parser')
            new_urls = list(
                filter(
                    lambda href: href is not None and href not in self.__queue,
                    map(
                        lambda a: self.__normalize_url(origin_url, a['href']),
                        soup.findAll('a', href=True)
                    )
                ))
            return new_urls
        except HTTPError:
            print("Error en la carga de la direccion: {}".format(origin_url))
        return list([])

    def __normalize_url(self, origin, url):
        """
        Normaliza las url dadas para validarlas
        :param origin: Url origen
        :param url: Url a normalizar
        :return: Url normalizada
        """
        if url.startswith('http'):
            return url
        elif url.startswith('//'):
            return 'https:' + url
        elif url.startswith('://'):
            return 'https' + url
        elif url.startswith('/'):
            return origin + url
        elif url.startswith('#'):
            return origin + url[1:]
        elif '/' is url or "" is url:
            return None

    def scanRobots(self, url, link):
        """ScanRobots
        Revisa el robots.txt y devuelve True en caso de que se pueda
        escanear la web y False en caso contrario
        Params:
            url, url base
            link, url a comprobar por robots.txt
        """
        if url.endswith('/'):
            url = url[:- 1]
        robots_url = url + '/robots.txt'

        self.__robot_parser.set_url(robots_url)
        self.__robot_parser.read()
        time.sleep(self.__sleep_time)

        if not self.__robot_parser.can_fetch(self.__crawler_name, link):
            print("(!) Cannot scrap {}".format(link))
            print("\t # Crawling {} is prohibited unless you have express written".format(link))
            return False
        return True

    def save(self, path):
        if self.__obtained_urls is not None:
            path_array = path.split(".")
            path = path_array[0] + type(self.__strategy).__name__ + path_array[-1]
            with open(os.getcwd() + "/" + path, 'w') as f:
                for key, value in self.__obtained_urls.items():
                    f.write('%s\n' % key)
                    while len(value) > 0:
                        f.write('\t%s\n' % value.popleft())
        return self
