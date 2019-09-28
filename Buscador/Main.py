from src.conf.Config import Config
from src.model.Finder import Finder


def save(elem, path):
    with open(path, 'w') as f:
        f.write(elem)


def main():
    config = Config()
    s = ""
    for query in config.get_queries():
        s += Finder(query, config.get_texts()).__str__()
    print(s)
    save(s, config.get_output())


if __name__ == '__main__':
    main()
