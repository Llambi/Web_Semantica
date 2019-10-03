from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import difflib
import io


class Scorer:

    def __init__(self, simhash=None, truth_file=None, train_file=None):
        self.simhash = simhash
        self.train_file = train_file
        self.expected_matches = self.read_truth(truth_file)

    def get_score(self, restrictiveness=None, ngram=0):
        index = self.create_index(self.train_file, restrictiveness, ngram)
        got_matches = self.get_matches(index)
        print("\n" + ">" * 80)
        print("- EXPECTED MATCHES")
        print("+ GOT MATCHES")
        print(">" * 80)
        self.print_matches_comparation(self.expected_matches, got_matches)
        print("<" * 80)
        return self.print_score(self.expected_matches, got_matches)

    def create_index(self, file, restrictiveness, ngram_len):
        index = {}
        with io.open(file, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                args = [line, restrictiveness]
                if ngram_len:
                    args.append(ngram_len)

                hash = self.simhash(line, restrictiveness, ngram_len).exec()

                try:  # Si no existe la key salta excepcion y a lcapturarla se crea la key
                    index[hash].append(line)
                except:
                    index[hash] = [line]
        return index

    def get_matches(self, index):
        return tuple(sorted([" == ".join(sorted(line.split(" ")[0] for line in lines)) for _, lines in index.items() if
                             len(lines) > 1]))

    def print_matches_comparation(self, expected_matches, got_matches):
        for line in difflib.ndiff(expected_matches, got_matches):
            print(line)

    def print_score(self, expected_matches, got_matches):
        s1 = set(expected_matches)
        s2 = set(got_matches)
        score = len(s1.intersection(s2)) / len(s1.union(s2))
        print("SCORE: {}".format(score))
        return score

    def read_truth(self, text):
        matches = []
        with io.open(text, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                matches.append(" == ".join(sorted(line.split(" "))))
        return tuple(sorted(matches))
