import string
import os
import numpy as np
import pickle
LA = np.linalg
from nltk.corpus import stopwords
from nltk.stem.porter import *

is_noun = lambda pos: pos[:2] == 'NN'
number = 10

Docs = list()

def NormalizeWord(f):
    return re.sub ( r"[^a-zA-Z]+", '', f ).strip()
# to get all the files in that directory
path = "./text-06_04-06_17.txt"
wordcount = {}
word_list = []
index = set ()
Counter = ()
inp = open(path, 'rb')
fil = pickle.load(inp)
inp.close()

s =" ".join(fil)
doc =[" ".join([word for word in s.lower().translate(str.maketrans('', '', string.punctuation)).split()if len(word) >=4])]
# stemdoc = " ".join(stemm.stem([y for y in[x for x in doc]]))
Docs.append(doc.__str__())





from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
import string
exclude = set(string.punctuation)
lemma = WordNetLemmatizer()
sw = set(stopwords.words('english'))
punctuation = re.compile(r'[\[?!"\'💀#*;+()@|0-9|\]|]')
def clean(doc):
    stop_free = " ".join([i for i in doc.lower().split() if i not in sw])
    word = stop_free.lower()
    word = word.replace(".", "")
    normalized = punctuation.sub("", word)
    if ((normalized.startswith("http") != -1) and len(normalized)<4):
        k=0
    else:
        normalized = normalized

    return normalized



doc_clean = [clean(doc).split() for doc in Docs]
#print(doc_clean)
print("completed")
import gensim
from gensim import corpora
dict = corpora.Dictionary(doc_clean)
TDM = [dict.doc2bow(doc) for doc in doc_clean]
print("yes")
Lda = gensim.models.ldamodel.LdaModel
print("doing LDA")
ldamodel = Lda(TDM, num_topics=3, id2word = dict, passes=50)
print(ldamodel.print_topic(0,number))




topics_matrix = ldamodel.show_topics(formatted=False, num_words=number)
i=1
for topic in topics_matrix:
    print("Topic "+i.__str__()+"::")
    sta=""
    for word in topic[1]:
        sta +=word[0]+"\t "
    i=i+1
    print(sta)


