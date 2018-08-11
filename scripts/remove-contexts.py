import os
import sys
import time
import logging
import argparse
from gensim.models import KeyedVectors

from helpers import mkdir_if_not_exists


def filter_file(deps_context_path, output_dirname, mode, vocab):
    with open(os.path.join(deps_context_path, mode), 'r', 65536) as input:
        with open(os.path.join(output_dirname, mode), 'w', 65536) as output:
            for line in input:
                line = line.strip()
                if '\t' in line or '=' in line:
                    continue
                tokens = line.split(' ')
                if mode == 'cv':
                    word = tokens[0].split('_')[1]
                elif mode == 'wv':
                    word = tokens[0]
                else:
                    word = tokens[0]
                    if word not in vocab:
                        continue
                    contexts = tokens[1:]
                    for context in contexts:
                        ctx_word = context.split('_')[1]
                        if ctx_word not in vocab:
                            continue
                        output.write('{} {}\n'.format(word,context))
                        continue
                    continue
                if word not in vocab:
                    continue
                output.write(line+'\n')

def main():
    logging.basicConfig(format='%(levelname)s: %(message)s')
    logging.getLogger().setLevel(logging.INFO)
    parser = argparse.ArgumentParser(prog=os.path.basename(sys.argv[0]),
                                     formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description=__doc__)
    parser.add_argument("input", help="deps_context_path")
    parser.add_argument("-o", "--output", default="./data/contexts/",
                        help="directory for extracted files")
    parser.add_argument("-m", "--model", default="./data/models/word2vec/word2vec-s400-w5-m5.bin",
                        help="word2vec model to extract vocab")

    args = parser.parse_args()
    output_dirname = args.output
    mkdir_if_not_exists(output_dirname)
    deps_context_path = args.input

    word_vectors = KeyedVectors.load_word2vec_format(args.model, binary=True)
    vocab = set(word_vectors.vocab)
    logging.info('Vocab:\t%d', len(vocab))

    extract_start = time.perf_counter()

    logging.info("Processing wv ...")
    filter_file(deps_context_path, output_dirname, 'wv', vocab)
    logging.info("Processing cv ...")
    filter_file(deps_context_path, output_dirname, 'cv', vocab)
    logging.info("Processing dep.contexts ...")
    filter_file(deps_context_path, output_dirname, 'dep.contexts', vocab)

    extract_duration = time.perf_counter() - extract_start
    logging.info("elapsed %f", extract_duration)


if __name__ == '__main__':
    main()


# python ./scripts/remove-contexts.py ./data/contexts/ -m ./data/models/word2vec/word2vec-s100-w5-m2-sg0.bin -o ./data/contexts2/
