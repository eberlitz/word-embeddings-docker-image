import os
from gensim.models import KeyedVectors
from gensim.test.utils import datapath, get_tmpfile
from gensim.scripts.glove2word2vec import glove2word2vec

fastTextModels = [
    "data/models/fastText/fasttext-s1000-m2-sg0.vec",
    "data/models/fastText/fasttext-s300-m2-sg0.vec",
    "data/models/fastText/fasttext-s600-m2-sg0.vec",
    "data/models/fastText/fasttext-s100-m2-sg0.vec",
    "data/models/fastText/fasttext-s50-m2-sg0.vec",
    "data/models/fastText/fasttext-s1000-m2-sg1.vec",
    "data/models/fastText/fasttext-s300-m2-sg1.vec",
    "data/models/fastText/fasttext-s600-m2-sg1.vec",
    "data/models/fastText/fasttext-s100-m2-sg1.vec",
    "data/models/fastText/fasttext-s50-m2-sg1.vec",
]

GloVeModels = [
    "data/models/GloVe/vectors-1000.txt",
    "data/models/GloVe/vectors-100.txt",
    "data/models/GloVe/vectors-300.txt",
    "data/models/GloVe/vectors-50.txt",
    "data/models/GloVe/vectors-600.txt",
]
wang2vec = [
    "data/models/wang2vec/wang2vec-s1000-m2-sg0",
    "data/models/wang2vec/wang2vec-s100-m2-sg1",
    "data/models/wang2vec/wang2vec-s50-m2-sg0",
    "data/models/wang2vec/wang2vec-s600-m2-sg1",
    "data/models/wang2vec/wang2vec-s1000-m2-sg1",
    "data/models/wang2vec/wang2vec-s300-m2-sg0",
    "data/models/wang2vec/wang2vec-s50-m2-sg1",
    "data/models/wang2vec/wang2vec-s100-m2-sg0",
    "data/models/wang2vec/wang2vec-s300-m2-sg1",
    "data/models/wang2vec/wang2vec-s600-m2-sg0",
]

word2vec = [
    "data/models/word2vec/word2vec-s1000-w5-m2-sg0.bin",
    "data/models/word2vec/word2vec-s300-w5-m2-sg0.bin",
    "data/models/word2vec/word2vec-s600-w5-m2-sg0.bin",
    "data/models/word2vec/word2vec-s1000-w5-m2-sg1.bin",
    "data/models/word2vec/word2vec-s300-w5-m2-sg1.bin",
    "data/models/word2vec/word2vec-s600-w5-m2-sg1.bin",
    "data/models/word2vec/word2vec-s100-w5-m2-sg0.bin",
    "data/models/word2vec/word2vec-s50-w5-m2-sg0.bin",
    "data/models/word2vec/word2vec-s100-w5-m2-sg1.bin",
    "data/models/word2vec/word2vec-s50-w5-m2-sg1.bin",
]
word2vecf = [
    "data/models/word2vecf/vecs-n15-s50",
    "data/models/word2vecf/vecs-n15-s100",
    "data/models/word2vecf/vecs-n15-s300",
    "data/models/word2vecf/vecs-n15-s600",
    "data/models/word2vecf/vecs-n15-s1000",
]


def main():
    total = len(fastTextModels) + len(GloVeModels) + \
        len(wang2vec) + len(word2vec) + len(word2vecf)
    print('Evaluating {} models'.format(total))
    evaluationCount = 0
    pairs = 'PT65.tsv'
    output_filename = './data/word_pairs_evaluation.txt'
    format_entry = '{0}:\n\t{1}\n\n'
    with open(output_filename, 'w', encoding='utf-8') as output:
        for path in fastTextModels:
            wv = KeyedVectors.load_word2vec_format(path, binary=False)
            result = wv.evaluate_word_pairs(pairs)
            output.write(format_entry.format(path, result))
            evaluationCount += 1
            print('Evaluating {}/{}'.format(evaluationCount, total))
        for path in GloVeModels:
            tmp_file = get_tmpfile("glove2w2v_" + os.path.basename(path))
            glove2word2vec(path, tmp_file)
            wv = KeyedVectors.load_word2vec_format(tmp_file)
            result = wv.evaluate_word_pairs(pairs)
            output.write(format_entry.format(path, result))
            os.remove(tmp_file)
            evaluationCount += 1
            print('Evaluating {}/{}'.format(evaluationCount, total))
        for path in wang2vec:
            wv = KeyedVectors.load_word2vec_format(path, binary=True)
            result = wv.evaluate_word_pairs(pairs)
            output.write(format_entry.format(path, result))
            evaluationCount += 1
            print('Evaluating {}/{}'.format(evaluationCount, total))
        for path in word2vec:
            wv = KeyedVectors.load_word2vec_format(path, binary=True)
            result = wv.evaluate_word_pairs(pairs)
            output.write(format_entry.format(path, result))
            evaluationCount += 1
            print('Evaluating {}/{}'.format(evaluationCount, total))
        for path in word2vecf:
            wv = KeyedVectors.load_word2vec_format(path, binary=False)
            result = wv.evaluate_word_pairs(pairs)
            output.write(format_entry.format(path, result))
            evaluationCount += 1
            print('Evaluating {}/{}'.format(evaluationCount, total))


if __name__ == '__main__':
    main()
