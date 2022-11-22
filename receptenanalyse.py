import matplotlib.pyplot as plt
import random
import time
import math
from tqdm import tqdm
from os import listdir
from os.path import isfile, join
from pdfminer.high_level import extract_text
import pandas as pd
import matplotlib.colors as colors
import matplotlib.patches as mpatches

from sklearn.cluster import DBSCAN

#	FUNCTIONS
def quickSaveUnicode(content, fn):
    with io.open(fn, "w", encoding="utf-8") as f:
        f.write(content)
def quickAppendUnicode(content, fn):
    with io.open(fn, "a", encoding="utf-8") as f:
        f.write(content)
def preprocess(text):
    r = ""
    for character in text:
        if not character in '“”[]()?,.;!:\"\'':
            r+=character
    return r.lower()

with open("stopwords.txt", 'r', encoding="utf-8") as f:
    stopwords = f.read().split('\n')
print(stopwords)

def similar(t1, t2): #sets as input
    i = len(t1.intersection(t2))
    u = len(t1.union(t2))
    return float(i)/u

def slashn(text):
    r = ""
    c = 0
    for character in text:
        c+=1
        if c%25==0:
            r+="-\n"
        r+=character
    return r

def normal(sigma, m, x):
    return (1/(sigma * math.sqrt(math.pi * 2)))*(math.exp(  - (((x-m)/sigma)**2)/2 ))

def fo(x):
    return x#math.log(x)
    #return 1 - math.floor(  100*math.sin(1-x)**10  )/7.

def remove_stopwords(l_of_words):
    res = []
    global stopwords
    for w in l_of_words:
        if not w in stopwords:
            res.append(w)
    return res



#	LOADING DATA
receptendict = {}

print("Loading data...")
with open("receptennotags.txt", 'r', encoding="utf-8") as f:
    d = f.read()
d2 = d.split("&")
recepten = []
for recept in d2:
    lines = recept.split('\n')
    lines = [l for l in lines if not l == '']
    recepten.append(lines)

recepten_naamen = 	[]
recepten_recept	= 	[]
for r in recepten:
    #print('recept: ', r[0])
    recepten_naamen.append(slashn(r[0]))
    recepten_recept.append(    remove_stopwords(( preprocess(' '.join(r[1:]))).split(' '))  )	
    receptendict[r[0]] = remove_stopwords(( preprocess(' '.join(r[1:]))).split(' '))
print("Computing similarity measure...")
matrix = []
similarities = []
for i in recepten_recept:
    r = []
    for j in recepten_recept:
        r.append( fo( similar(set(i),set(j)) ) )
        similarities.append(similar(set(i),set(j)))
    matrix.append(r)
        
#plt.plot(sorted([   similarities_stopwords[i] - similarities[i]   for i in range(len(similarities))])  ,  color="red", linewidth="1")

#plt.ylabel("Similarity")
#plt.xlabel("pairs (text1, text2)")
#plt.title("(Sorted) similarity differences (with stopwords vs no stop words)")
#plt.savefig("similaritiesdifference.png",dpi=300.)
#plt.show()
#quit()


print("Running DBSCAN...")
clustering = DBSCAN(eps=1.03, min_samples=1).fit_predict(matrix)
print(clustering)

clusters = {}
naamen = [''.join(r.split("-\n")) for r in recepten_naamen]

for i in range(len(clustering)):
    if clustering[i] in list(clusters.keys()):
        clusters[clustering[i]].append(naamen[i])
    else:
        clusters[clustering[i]] = [naamen[i]]
        
sorted_naamen = []
for c in list(clusters.values()):
    for cc in c:
        sorted_naamen.append(cc)
print(sorted_naamen)

sorted_recepten = []
for naam in sorted_naamen:
    sorted_recepten.append(receptendict[naam])

matrix = []
similarities = []
for i in sorted_recepten:
    rr = []
    for j in sorted_recepten:
        rr.append( fo( similar(set(i),set(j)) ) )
        similarities.append(similar(set(i),set(j)))
    matrix.append(rr)



df = pd.DataFrame( matrix,
                   columns = sorted_naamen,
                   index = sorted_naamen)



plt.title(f"Lexical similarity of {len(recepten_naamen)} https://www.leukerecepten.nl/ recipes\n (no stop words, sorted, DBSCAN(eps=1.03, min_samples=1))")
plt.imshow(df, cmap="YlGnBu")
plt.colorbar()
plt.xticks(range(len(df)),df.columns, rotation=90, fontsize=1)
plt.yticks(range(len(df)),df.index, fontsize=1)

plt.savefig("lekker_"+str(time.time())+".png", dpi=600.)

plt.show()

