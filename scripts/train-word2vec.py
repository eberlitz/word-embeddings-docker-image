#!/usr/bin/python
import os
import re
import sys
import bz2
import glob
import gensim
import logging
import argparse
import collections
import multiprocessing
from helpers import mkdir_if_not_exists

logging.basicConfig(
    format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


class MySentences(object):
    def __init__(self, dirname):
        self.dirname = dirname

    def __iter__(self):
        filepaths = glob.glob(self.dirname)
        filepaths.sort()
        for fp in filepaths:
            with bz2.BZ2File(fp, 'r') as input:
                for line in input:
                    yield line.decode('utf-8').split()


def main():
    parser = argparse.ArgumentParser(prog=os.path.basename(sys.argv[0]),
                                     formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description=__doc__)
    parser.add_argument("input", help="ptwiki-compressed-text-folder")
    parser.add_argument("-o", "--output", default="./models/",
                        help="directory for extracted files")
    parser.add_argument("-s", "--size", type=int, default=200,
                        help="size")
    parser.add_argument("-w", "--window", type=int, default=5,
                        help="window")
    parser.add_argument("-m", "--mincount", type=int, default=2,
                        help="mincount")
    parser.add_argument("-sg", "--sg", type=int, default=0,
                        help="use skip-gram")

    args = parser.parse_args()
    output_dirname = args.output
    input_dir = args.input
    size = args.size
    sg = args.sg
    window = args.window
    min_count = args.mincount
    output_path = args.output

    mkdir_if_not_exists(output_dirname)

    # '../data/ptwiki-articles-text-preprocessed
    wiki_text_dump_path = input_dir+'/**/*.bz2'
    sentences = MySentences(wiki_text_dump_path)

    mkdir_if_not_exists(output_path)

    # build vocabulary and train model
    model = gensim.models.Word2Vec(sentences,
                                   size=size,
                                   window=window,
                                   min_count=min_count,
                                   sg=sg,
                                   workers=multiprocessing.cpu_count())

    # model.train(documents, total_examples=len(documents), epochs=10)

    # trim unneeded model memory = use (much) less RAM
    # Precompute L2-normalized vectors.
    # If replace is set, forget the original vectors and only keep the normalized ones = saves lots of memory!
    # Note that you cannot continue training after doing a replace. The model becomes effectively read-only = you can call most_similar, similarity etc., but not train.
    model.init_sims(replace=True)

    model_file_name = os.path.join(
        output_path, 'word2vec-s{0}-w{1}-m{2}-sg{3}'.format(size, window, min_count, sg))
    # model.save(model_file_name)
    model.wv.save_word2vec_format(
        '{0}.bin'.format(model_file_name), binary=True)

    word_vectors = model.wv
    # word_vectors.save(output_path)

    print(word_vectors.most_similar(positive=['carro'], topn=10))
    print("Most similar to {0}".format(
        word_vectors.most_similar(positive="america")))
    print('CONCLUDED')


if __name__ == '__main__':
    main()
