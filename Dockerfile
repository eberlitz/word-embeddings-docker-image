FROM python:3.6
MAINTAINER Eduardo Eidelwein Berlitz "eberlitz@gmail.com"

USER root

WORKDIR /usr/src/app

ADD ./word2vecf.tar ./
WORKDIR /usr/src/app/word2vecf
RUN make
WORKDIR /usr/src/app

ADD ./wang2vec.tar ./
WORKDIR /usr/src/app/wang2vec
RUN make
WORKDIR /usr/src/app

ADD ./fastText.tar ./
WORKDIR /usr/src/app/fastText
RUN make
WORKDIR /usr/src/app

ADD ./GloVe.tar ./
WORKDIR /usr/src/app/GloVe
RUN make
WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY ./scripts ./scripts

COPY glove.sh ./

COPY ./PT65.tsv ./
