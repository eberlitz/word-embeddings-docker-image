
```sh
# Build the image
docker build -t eberlitz/ptwiki2vec .

# Generate word2vecf input files
docker run -it -v /home/berlitz/data:/usr/src/app/data eberlitz/ptwiki2vec python ./scripts/multiprocess_contexts.py ./data/ptwiki.db -o ./data/contexts/ -b 1000

# train word2vecf
docker run -it -v /home/berlitz/data:/usr/src/app/data eberlitz/ptwiki2vec ./word2vecf/word2vecf -train ./data/contexts2/dep.contexts -wvocab ./data/contexts2/wv -cvocab ./data/contexts2/cv -output ./data/models/word2vecf/vecs-n15-s50 -negative 15 -threads 31 -size 50
docker run -it -v /home/berlitz/data:/usr/src/app/data eberlitz/ptwiki2vec python ./scripts/vecs2nps.py ./data/models/word2vecf/vecs-n15-s50 ./data/models/word2vecf/vecs-n15-s50

# train word2vec models
curl https://eberlitz.blob.core.windows.net/ptwiki2vec/data/ptwiki-articles-text-preprocessed.tar.gz -o ./data/ptwiki-articles-text-preprocessed
docker run -it -v /home/berlitz/data:/usr/src/app/data eberlitz/ptwiki2vec python ./scripts/train-word2vec.py ./data/ptwiki-articles-text-preprocessed -o ./data/models/word2vec/ --window 5 --mincount 2 --sg 0 --size 50

# generate a single txt file from compressed files folder
docker run -it -v /home/berlitz/data:/usr/src/app/data eberlitz/ptwiki2vec python ./scripts/to-single-txt.py ./data/ptwiki-articles-text-preprocessed/ -o ./data/ptwiki-preprocessed-all.txt

# prune out of vocab words from word2vecf input files
docker run -it -v /home/berlitz/data:/usr/src/app/data eberlitz/ptwiki2vec python ./scripts/remove-contexts.py ./data/contexts/ -m ./data/models/word2vec/word2vec-s100-w5-m2-sg0.bin -o ./data/contexts2/

```

docker run -it -v /home/berlitz/data:/usr/src/app/data eberlitz/ptwiki2vec ./fastText/fasttext cbow -input ./data/ptwiki-preprocessed-all.txt -thread 31 -minCount 2 -output ./data/models/fastText/fasttext-s50-m2-sg0 -dim 50
docker run -it -v /home/berlitz/data:/usr/src/app/data eberlitz/ptwiki2vec ./fastText/fasttext skipgram -input ./data/ptwiki-preprocessed-all.txt -thread 31 -minCount 2 -output ./data/models/fastText/fasttext-s1000-m2-sg1 -dim 1000

docker run -it -v /home/berlitz/data:/usr/src/app/data eberlitz/ptwiki2vec ./wang2vec/word2vec -train ./data/ptwiki-preprocessed-all.txt -output ./data/models/wang2vec/wang2vec-s50-m2-sg0 -type 0 -window 5 -min-count 2 -threads 31 -binary 1 -iter 5 -size 50

docker run -it -v /home/berlitz/data:/usr/src/app/data eberlitz/ptwiki2vec ./wang2vec/word2vec -train ./data/ptwiki-preprocessed-all.txt -output ./data/models/wang2vec/wang2vec-s50-m2-sg1 -type 1 -window 5 -min-count 2 -threads 31 -binary 1 -iter 5 -size 50


docker run -it -v /home/berlitz/data:/usr/src/app/data eberlitz/ptwiki2vec sh ./glove.sh ./data/ptwiki-preprocessed-all.txt ./data/glove