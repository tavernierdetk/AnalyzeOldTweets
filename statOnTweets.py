#!/usr/bin/python2.7
import csv
from nltk.corpus import stopwords
import re
import string
from collections import defaultdict


def countAndClean(fileToClean):
    stop = stopwords.words('english')
    stop.append('ie')

    inter1 = []
    sentences_all = []
    sentences_clean = []
    sentences_unpun = []

    dictionary1 = {}
    d2_dict = defaultdict(dict)

    with open(fileToClean) as f:
        rows = csv.reader(f, delimiter = ',')
        for row in rows:
            inter1.append(row[1])

    for row in inter1:
        sentences = re.split(r' *[\.\?!][\'"\)\]]* *', row)

        for s in sentences:
            in1 = ''.join(s)
            out = re.sub('[%s]' % re.escape(string.punctuation), '', in1.lower())
            sentences_all.append(out)

    for sentence in sentences_all:
        s = []
        for i in sentence.split():
            if i not in stop:
                s.append(i)
        sentences_clean.append(s)

    for sentence in sentences_clean:
        #print sentence
        for word in sentence:
            dictionary1[word] = 0

    for sentence in sentences_clean:
        for word in sentence:
            dictionary1[word] = dictionary1[word] + 1

    for sentence in sentences_clean:
        for word in sentence:
            for word2 in sentence:
                if(word != word2):
                    d2_dict[word][word2] = 0

    for sentence in sentences_clean:
        for word in sentence:
            for word2 in sentence:
                if(word != word2):
                    d2_dict[word][word2] = d2_dict[word][word2] + 1

    with open('word_freq.csv', mode='w') as tweetCollection:
        writer = csv.writer(tweetCollection, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for key, value in dictionary1.items():
            writer.writerow([key, value])


    with open('word_pair_freq.csv', mode='w') as tweetCollection:
        writer = csv.writer(tweetCollection, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for key1, value1 in d2_dict.items():
            for key2, value2 in d2_dict[key1].items():
                writer.writerow([key1, key2, value2])
        print ("Wrote to: ")

if __name__ == "__main__":
    countAndClean('all_tweets.csv')