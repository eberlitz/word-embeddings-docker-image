
```sh
# Build the image
docker build -t word2vecf:latest .

# Generate word2vecf input files
docker run -it -v /home/berlitz/data:/usr/src/app/data word2vecf:latest python ./scripts/multiprocess_contexts.py ./data/ptwiki.db -o ./data/contexts/ -b 1000

# train word2vecf
docker run -it -v /home/berlitz/data:/usr/src/app/data word2vecf:latest ./word2vecf/word2vecf -train ./data/contexts/dep.contexts -wvocab ./data/contexts/wv -cvocab ./data/contexts/cv -output ./data/dim200vecs -size 200 -negative 15 -threads 10

# convert to numpy vectors
docker run -it -v /home/berlitz/data:/usr/src/app/data word2vecf:latest python ./scripts/vecs2nps.py ./data/dim200vecs ./data/vecs

# train word2vec models
curl https://eberlitz.blob.core.windows.net/ptwiki2vec/data/ptwiki-articles-text-preprocessed.tar.gz -o ./data/ptwiki-articles-text-preprocessed

docker run -it -v /home/berlitz/data:/usr/src/app/data word2vecf:latest python ./scripts/train-word2vec.py ./data/ptwiki-articles-text-preprocessed ./models/word2vec/ -size 200 -window 5 -mincount 2

```
