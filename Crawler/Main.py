from conf.config import Config
from model.Crawler import Crawler


def main():
    config = Config()
    Crawler(config.get_url_list(), config.get_args().name, config.get_args().d,
            config.get_args().mx, config.get_args().sec).craw().save(config.get_args().output)


if __name__ == '__main__':
    main()
