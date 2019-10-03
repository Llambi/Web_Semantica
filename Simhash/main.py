import csv

from conf.Config import Config
from model.Scorer import Scorer


def write_csv(scorer, file):
    with open(file, 'w') as csvfile:
        writer = csv.writer(csvfile, delimiter=str(';'), quotechar=str('|'), quoting=csv.QUOTE_MINIMAL)
        writer.writerow(['R'] + ([str(i) for i in range(1, 11)]))
        for restrictiveness in range(1, 20):
            row = [restrictiveness]
            for ngram in range(1, 11):
                score = scorer.get_score(restrictiveness, ngram)
                row.append("%.4f" % round(score, 4))
            writer.writerow(row)


def main():
    config = Config()
    args = config.get_args()
    simhash = config.get_classes()['Simhash'].Simhash.Simhash
    Scorer(simhash, args.truth, args.train).get_score(5, 4)
    return 0


def testNgram():
    config = Config()
    args = config.get_args()
    simhash = config.get_classes()['Simhash'].Simhash.Simhash
    write_csv(Scorer(simhash, args.truth, args.train), args.output)


if __name__ == '__main__':
    main()
