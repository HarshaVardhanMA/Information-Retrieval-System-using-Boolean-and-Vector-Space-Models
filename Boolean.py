import sys
from nltk.stem.porter import *
import os
import re
from collections import Counter
from nltk.tokenize import word_tokenize
from nltk.stem.porter import *
from os import listdir
from os.path import isfile, join

def words(text): return re.findall(r'\w+', text.lower())

stemmer = PorterStemmer()
invin = {}
filenamedict = {}
files = {}
i=0
print(sys.argv[1])
onlyfiles = [f for f in listdir(str(sys.argv[1])) if isfile(join(str(sys.argv[1]), f))]
#print(onlyfiles)
n = len(onlyfiles)
final=[]
stemmer = PorterStemmer()
for i in range(0,len(onlyfiles)):
    with open(os.path.abspath(os.path.join(sys.argv[1],onlyfiles[i]))) as file:
        for line in file:
            wordsinaline = word_tokenize(line)
            final.extend(j for k in wordsinaline for j in k)
            wordsinaline = [stemmer.stem(plural) for plural in wordsinaline]
            for eachword in wordsinaline:
                #print (eachword)

                if eachword not in invin:
                    setofaword = set()
                    setofaword.add(onlyfiles[i])
                    eachwordstr = stemmer.stem(eachword.strip())
                    if (eachword.startswith('"') or eachword.startswith("'")) and (eachword.endswith('"') or eachword.endswith("'")):
                        eachwordstr = eachwordstr[1:-1]
                    invin[eachwordstr]=setofaword

                else:
                    setofanexistingword = invin.get(eachword)
                    if i not in setofanexistingword:
                        setofanexistingword.add(onlyfiles[i])


string = " ".join(str(x) for x in final)
WORDS = Counter(words(string))
#print(invin)
def P(word, N=sum(WORDS.values())):
    "Probability of `word`."
    return WORDS[word] / N

def correction(word):
    "Most probable spelling correction for word."
    return max(candidates(word), key=P)

def candidates(word):
    "Generate possible spelling corrections for word."
    return (known([word]) or known(edits1(word)) or known(edits2(word)) or [word])

def known(words):
    "The subset of `words` that appear in the dictionary of WORDS."
    return set(w for w in words if w in WORDS)

def edits1(word):
    "All edits that are one edit away from `word`."
    letters    = 'abcdefghijklmnopqrstuvwxyz'
    splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
    deletes    = [L + R[1:]               for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
    replaces   = [L + c + R[1:]           for L, R in splits if R for c in letters]
    inserts    = [L + c + R               for L, R in splits for c in letters]
    return set(deletes + transposes + replaces + inserts)

def edits2(word):
    "All edits that are two edits away from `word`."
    return (e2 for e1 in edits1(word) for e2 in edits1(e1))

#print(invin)

queryfile = open(sys.argv[2])
#print(sys.argv[2])
#print ("queryfile",queryfile.read())
operators = ["AND", "OR", "NOT"]
for queryline in queryfile:
    print ("Query :", queryline.rstrip())
    tempset = set()
    #print (queryline)
    splitatspace = queryline.split()
    #print ("before quote removal splitatspace", splitatspace)
    for w in range(0,len(splitatspace)):
            splitatspace[w]=correction(splitatspace[w])
    for i in range(len(splitatspace)):
        if (splitatspace[i].startswith('"') or splitatspace[i].startswith("'")) and (splitatspace[i].endswith('"') or splitatspace[i].endswith("'")):
            splitatspace[i] = splitatspace[i][1:-1]
    #print("after quote removal splitatspace", splitatspace)

    if len(splitatspace) == 0:
        print ("no query")
    elif len(splitatspace) == 1:
        if splitatspace[0].strip() not in operators:
            if stemmer.stem(splitatspace[0].strip()) in invin.keys():
                files = invin.get(stemmer.stem(splitatspace[0].strip()))
                print ("Results for query",' ',queryline.rstrip(),' ',"is :",files)

            else:
                print (splitatspace[0],"not in dict")
            #for file in files:
                #print(filenamedict[file], end=" ")
            print("\n")
        else:
            print ("only operator found")

    elif len(splitatspace) == 2 and splitatspace[0] == "NOT":
        if stemmer.stem(splitatspace[1].strip()) in invin.keys():
            #print ("splitatspace[1]", splitatspace[1])
            #print ("b", invin.get((stemmer.stem(splitatspace[1].strip()))))
            if stemmer.stem(splitatspace[1].strip()) in invin.keys():
                files = set(onlyfiles) - invin.get((stemmer.stem(splitatspace[1].strip())))
                print ("files", files )
            else:
                print (splitatspace[1], "not in dict")
            #for file in files:
                #print(filenamedict[file], end=" ")
            print("\n")

    elif len(splitatspace) == 2 and splitatspace[0] != "NOT":
        print ("invalid query")

    elif len(splitatspace) > 2:
        #print ("greater than 2")
        if(splitatspace[0].strip() not in operators):
            #print ("first element not an operator")
            if stemmer.stem(splitatspace[0].strip()) in invin.keys():
                tempset = invin.get(stemmer.stem(splitatspace[0].strip()))
                #print ("tempset ", tempset)
            else:
                print (splitatspace[0],"not in dict, partial results may be shown")
            loopstart = 1
            #print ("made loopstart 1")

        elif splitatspace[0].strip() == "NOT":

            if stemmer.stem(splitatspace[1].strip()) in invin.keys():
                tempset = set(range(1,4)) - invin.get((stemmer.stem(splitatspace[1].strip())))
            else:
                print (splitatspace[1],"not in dict, partial results may be shown")
            loopstart = 2

        elif splitatspace[0].strip() == "AND" or "OR":
            print ("invalid query")

        #print ("Loopstart", loopstart)
        #print ("len(splitatspace)", len(splitatspace))
        i = loopstart
        while(i<len(splitatspace)):
            #print ("in while")
            #print ("splitatspace[i] ",splitatspace[i])

            if splitatspace[i].strip() in operators:
                #print ("splitatspace[i] ",splitatspace[i],"is an operator")
                if splitatspace[i+1].strip() != "NOT":

                    if splitatspace[i].strip() == "AND" and splitatspace[i+1].strip() not in operators:
                        #print("splitatspace[i] is an AND")
                        if stemmer.stem(splitatspace[i+1].strip()) in invin.keys():
                            tempset = set.intersection(tempset,invin.get((stemmer.stem(splitatspace[i+1].strip()))))
                            #print ("tempset", tempset)
                        else:
                            print (splitatspace[i+1], "not in dict, partial results may be shown")
                    if splitatspace[i].strip() == "OR" and splitatspace[i+1].strip() not in operators:
                        #print("splitatspace[i] is an OR")
                        if stemmer.stem(splitatspace[i+1].strip()) in invin.keys():
                            tempset = set.union(tempset,invin.get((stemmer.stem(splitatspace[i+1].strip()))))
                        else:
                            print(splitatspace[i + 1], "not in dict, partial results may be shown")

                    #for queries like aaaa NOT bbbb
                    if splitatspace[i] == "NOT":

                        print ("invalid query, partial results may be shown")
                    i = i+2
                    #print ("i = i+2", i)

                elif splitatspace[i+1].strip() == "NOT" and splitatspace[i+2].strip() not in operators:
                    print ("i+1 is NOT, elif")
                    if stemmer.stem(splitatspace[i+2].strip()) in invin.keys():
                        tempset2 = set(range(1,4)) - invin.get((stemmer.stem(splitatspace[i+2].strip())))
                    else:
                        print (splitatspace[i+2], "not in dict, partial results may be shown")
                        #break

                    if splitatspace[i].strip() == "AND":
                        tempset = set.intersection(tempset,tempset2)

                    if splitatspace[i].strip() == "OR":
                        tempset = set.union(tempset,tempset2)

                    i = i+3
                    #print ("i = i+3", i)

            else:
                print ("invalid query, partial results are shown")
                break
    
        if len(tempset) == 0:
            print("Results for query",' ',queryline.rstrip(),' ',"is : nothing to display")
            print ("\n")
        else:
            print ("Results for query",' ',queryline.rstrip(),' ',"is :",tempset)
            print ("\n")
        
            
    #for file in tempset:
        #print(filenamedict[file])
    

#print (queryfile.read())

#print (invin)






