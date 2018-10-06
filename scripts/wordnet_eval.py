import nltk
from nltk.corpus import wordnet as wn
from itertools import product
from gensim.utils import smart_open, to_unicode
from scipy import stats
# nltk.download("omw");
# nltk.download("wordnet");


def calcSim(w1, w2, fn):
    allsyns1 = set(wn.synsets(w1, lang="por")[:])
    allsyns2 = set(wn.synsets(w2, lang="por")[:])
    if len(allsyns1) > 0 and len(allsyns2) > 0:
        best = max((fn(s1, s2) or 0, s1, s2)
                   for s1, s2 in product(allsyns1, allsyns2) if w1 == w2 or s1 != s2)
        return best[0]
    else:
        return None

def wupSim(w1, w2):
    return calcSim(w1, w2, wn.wup_similarity)

def lchSim(w1, w2):
    return calcSim(w1, w2, wn.lch_similarity)

def pathSim(w1, w2):
    return calcSim(w1, w2, wn.path_similarity)


def evaluate_word_pairs(pairs, fn):
    delimiter = '\t'
    similarity_gold = []
    similarity_model_wup = []
    oov = 0
    for line_no, line in enumerate(smart_open(pairs)):
        line = to_unicode(line.strip())
        a, b, sim = [word for word in line.split(delimiter)]
        sim = float(sim)
        wup = fn(a, b)
        if wup == None:
            oov += 1
            continue
        similarity_gold.append(sim)
        similarity_model_wup.append(wup)

    spearman = stats.spearmanr(similarity_gold, similarity_model_wup)
    pearson = stats.pearsonr(similarity_gold, similarity_model_wup)
    oov_ratio = float(oov) / (len(similarity_gold) + oov) * 100
    return (pearson, spearman, oov_ratio,)


def main():
    pairs = 'PT65.tsv'
    print(evaluate_word_pairs(pairs, wupSim))
    print(evaluate_word_pairs(pairs, pathSim))
    # print(evaluate_word_pairs(pairs, lchSim))


# ((0.6224196059044503, 3.9086124786740125e-07), SpearmanrResult(correlation=0.5993354805660435, pvalue=1.3336702025718145e-06), 15.384615384615385)
# ((0.7629920696961829, 1.2781571648596962e-11), SpearmanrResult(correlation=0.638215045981246, pvalue=1.5911706121638655e-07), 15.384615384615385)

if __name__ == '__main__':
    main()
