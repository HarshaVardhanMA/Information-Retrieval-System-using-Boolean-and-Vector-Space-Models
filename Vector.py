from os import listdir
from os.path import isfile, join
import sys
import os
import re
from collections import Counter
from nltk.tokenize import word_tokenize
from nltk.stem.porter import *
import math


def get_cosine(vec1, vec2):
     if len(vec1)==0:
         return 0
     intersection = set(vec1.keys()) & set(vec2.keys())
     sum=0.0
     for x in intersection:
          sum = sum+(vec1[x] * vec2[x])
     numerator = sum
     sum=0.0
     for x in vec1.keys():
         sum = sum+(vec1[x]**2)
     sum1 = sum
     sum=0.0
     for x in vec2.keys():
         sum = sum+(vec2[x]**2)
     sum2 = sum
     denominator = (math.sqrt(sum1) * math.sqrt(sum2))

     if not denominator:
        return 0.0
     else:
        return float(numerator) / denominator



print(sys.argv[1])
onlyfiles = [f for f in listdir(str(sys.argv[1])) if isfile(join(str(sys.argv[1]), f))]
print(onlyfiles)
n = len(onlyfiles)
#final=[]
docs_and_freq={}#stores docs and term frequencies
word_freq_inDoc={}#stores Word and its frequencies
#term_freq={}
stemmer = PorterStemmer()
for i in range(0,n):
    string_array=[] #to store each line in file
    with open(os.path.abspath(os.path.join(sys.argv[1],onlyfiles[i]))) as file:
        for line in file:
            string_array.append(line)
    #print(test_array)
    allwords_one_file=[]#to store all elements in single array
    term_freq={}
    uniq_words={}
    token_sent=[word_tokenize(j) for j in string_array]
    #print(token_sent)
    #convertin 2D array to 1D
    allwords_one_file.extend(j for k in token_sent for j in k)
    #normalized tokens in each file
    singles = [stemmer.stem(plural) for plural in allwords_one_file]
    #calculating term frequency
    for ter in range(0,len(singles)):
        if singles[ter] in term_freq :
            t =term_freq[singles[ter]]
            term_freq[singles[ter]]=t+1
        else:
            term_freq[singles[ter]]=1;
        if singles[ter] not in uniq_words: # taking all unique Words
            uniq_words[singles[ter]] = True;
    docs_and_freq[onlyfiles[i]] = term_freq;#assigning tf of file to it's name
    #print(uniq_words)
    #claculating doc frequency
    for w,v in uniq_words.items():
        if w in word_freq_inDoc:
            t = word_freq_inDoc[w]
            word_freq_inDoc[w] = t+1
        else:
            word_freq_inDoc[w]=1
#print(docs_and_freq)
#print(word_freq_inDoc)
tf_idf={}

for file in docs_and_freq:
    tf_idf[file]={}
    temp = tf_idf[file]
    for w,val in docs_and_freq[file].items():
        temp[w]=((1+math.log10(val))*math.log10(len(onlyfiles)/ word_freq_inDoc[w]))

#print(tf_idf)
print(sys.argv[2])
q_string_array=[] #to store each line in file
with open(os.path.abspath(sys.argv[2])) as file:
        for line in file:
            q_string_array.append(line)
            q_term_freq={}
            q_token_sent=word_tokenize(line)
            #print(q_token_sent)
            #normalized tokens in each file
            q_singles = [stemmer.stem(plural) for plural in q_token_sent]
            for ter in range(0,len(q_singles)):
                if q_singles[ter] in q_term_freq :
                    t =q_term_freq[q_singles[ter]]
                    q_term_freq[q_singles[ter]]=t+1
                else:
                    q_term_freq[q_singles[ter]]=1;
            #print(q_term_freq)
            q_tf_idf={}
            for w,v in q_term_freq.items():
                if w in word_freq_inDoc:
                    q_tf_idf[w]=((1+math.log10(v))*math.log10(len(onlyfiles)/ word_freq_inDoc[w]))
                else:
                    q_tf_idf[w]=0
            result={}
            #print(q_tf_idf)
            for file,v in tf_idf.items():
                sum=0.0
                result[file]=get_cosine(q_tf_idf, tf_idf[file])
            result = [(k, result[k]) for k in sorted(result, key=result.get, reverse=True)]
            print(result[0])
