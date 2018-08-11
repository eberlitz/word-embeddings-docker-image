
```sh
# Build the image
docker build -t eberlitz/ptwiki2vec .

# Generate word2vecf input files
docker run -it -v /home/berlitz/data:/usr/src/app/data eberlitz/ptwiki2vec python ./scripts/multiprocess_contexts.py ./data/ptwiki.db -o ./data/contexts/ -b 1000

# train word2vecf
docker run -it -v /home/berlitz/data:/usr/src/app/data eberlitz/ptwiki2vec ./word2vecf/word2vecf -train ./data/contexts/dep.contexts -wvocab ./data/contexts/wv -cvocab ./data/contexts/cv -output ./data/dim200vecs -size 200 -negative 15 -threads 10

# convert to numpy vectors
docker run -it -v /home/berlitz/data:/usr/src/app/data eberlitz/ptwiki2vec python ./scripts/vecs2nps.py ./data/dim200vecs ./data/vecs

# train word2vec models
curl https://eberlitz.blob.core.windows.net/ptwiki2vec/data/ptwiki-articles-text-preprocessed.tar.gz -o ./data/ptwiki-articles-text-preprocessed
docker run -it -v /home/berlitz/data:/usr/src/app/data eberlitz/ptwiki2vec python ./scripts/train-word2vec.py ./data/ptwiki-articles-text-preprocessed -o ./data/models/word2vec/ --window 5 --mincount 2 --sg 0 --size 50

# generate a single txt file from compressed files folder
docker run -it -v /home/berlitz/data:/usr/src/app/data eberlitz/ptwiki2vec python ./scripts/to-single-txt.py ./data/ptwiki-articles-text-preprocessed/ -o ./data/ptwiki-preprocessed-all.txt

# prune out of vocab words from word2vecf input files
docker run -it -v /home/berlitz/data:/usr/src/app/data eberlitz/ptwiki2vec python ./scripts/remove-contexts.py ./data/contexts/ -m ./data/models/word2vec/word2vec-s100-w5-m2-sg0.bin -o ./data/contexts2/

```
