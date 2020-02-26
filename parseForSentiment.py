#!/usr/bin/python2.7
# change input file name in line 18 as appropriate, text must be in column 3.
# output file is called limit_post.csv. Change this name before you run the script each time.
import csv
from nltk.corpus import stopwords
import re
import string

def calculateSentimentScore(filePath, candidate, attribute, nbWords,outputFile):
    stop = stopwords.words('english')
    stop.append('ie')

    inter1 = []
    posts_clean = []
    posts = []
    posts_found_with_entity = []
    limited_post = []
    limited_post2 = []

    with open(filePath) as f:
        rows = csv.reader(f, delimiter = ',')
        for row in rows:
            inter1.append(row[1])

    for row in inter1:
        sentences_all = []
        sentences = re.split(r' *[\.\?!][\'"\)\]]* *', row)
        for s in sentences:
            in1 = ''.join(s)
            out = re.sub('[%s]' % re.escape(string.punctuation), '', in1.lower())
            sentences_all.append(out)
        posts.append(sentences_all)

    for post in posts:
        sentences_clean = []
        for sentence in post:
            s = []
            for i in sentence.split():
                if i not in stop:
                    s.append(i)
            sentences_clean.append(s)
        posts_clean.append(sentences_clean)

    nb = candidate
    nb2 = attribute
    nb3 = nbWords

    for post in posts_clean:
        for sentence in post:
            x = 0
            for i in sentence:
                if(i == nb):
                    x = 1
                    posts_found_with_entity.append(post)
                    break
            if(x == 1):
                break

    limit = nb3 + 1

    for post in posts_found_with_entity:
        sentence_with_attribute = []
        position_in_sentences = []
        for sentence in post:
            position  = 0
            for i in sentence:
                if(i == nb2):
                    position_in_sentences.append(position)
                    sentence_with_attribute.append(sentence)
                position = position + 1
        j = 0
        for sentence in sentence_with_attribute:
            limited_sentence = []
            for i in range(len(sentence)):
                if(abs(i - position_in_sentences[j]) < limit):
                    limited_sentence.append(sentence[i])
            j = j + 1
            limited_post.append(limited_sentence)

    for sent in limited_post:
        limited_post2.append(' '.join(sent))


    with open(outputFile, mode='w') as tweetCollection:
        out = csv.writer(tweetCollection, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for sent in limited_post2:
            out.writerow([sent])
    f.close()

    print ("Written to: " + outputFile)

if __name__ == "__main__":

    candidates = ['bernie','bloomberg']
    issues = ['economy','climate','immigration']
    for candidate in candidates:
        for issue in issues:
            outputfile = './SentimentFiles/'+candidate+issue+'.csv'
            calculateSentimentScore('all_tweets.csv',candidate,issue,7,outputfile)