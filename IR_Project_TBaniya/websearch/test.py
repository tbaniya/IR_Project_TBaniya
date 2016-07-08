#!/Python34/python
import cgi
#key_words = []
form = cgi.FieldStorage()                 # parse form data
print('Content-type: text/html\n')        # hdr plus blank line
print('<title>Reply Page</title>')        # html reply page
if not 'key_word' in form:
    print('<h1>Enter the word to search?</h1>')
else:
    #print('<h1>word you enter : <i>%s</i>!</h1>' % cgi.escape(form['key_word'].value))
    key_words = cgi.escape(form['key_word'].value).split(" ")
    print(key_words)


import math
import os
from nltk.stem import PorterStemmer
from collections import OrderedDict



# using porterStemmer to remove morphological variations
stemmer = PorterStemmer()

    
count = 0
index_Hash = {}
def makeIndex(filepath):
    global count
    filelist = os.listdir(filepath)
    for filename in filelist:
        #tmp_hash stores word type and frequency in each document
        tmp_hash = {}
        count += 1
        file = open(filepath + filename,'r')
        # the first line of each file store the link to page, escape that line
        for i in range(2):
            file.readline()
        for line in file:
            word = line.strip()
            if word not in tmp_hash:
                tmp_hash[word] = 1
            else:
                tmp_hash[word] += 1
         # for each word in tmp_hash, check if in index_Hash and store       
        for w in tmp_hash:
            if w not in index_Hash:
                tmp = {}
                tmp[filename] = tmp_hash[w]
                index_Hash[w] = tmp
            else:
                tmp = {}
                tmp = index_Hash[w]
                tmp[filename] = tmp_hash[w]
                index_Hash[w] = tmp
                
    file.close()            
    
filepath = "./processedFiles/"
# the dirctory which stores the preprocessed files is the input to the method makeIndex()

makeIndex(filepath)


Retrieved_list = {}
LQsqr = 0.0
L = 0.0
LDsqr = 0.0

for each_token in key_words:
    each_token = stemmer.stem(each_token).lower()
    if each_token in index_Hash:
        doc_hash = {}
        doc_hash = index_Hash[each_token]
        K = query.count(each_token)
        m = len(doc_hash)
        I = math.log2(count/m)
        W = K * I
        LQsqr += W*W
        
        for doc in doc_hash:
            C = doc_hash[doc]
            
            if doc not in Retrieved_list:
                score = 0.0
                score += W* I * C
                LDsqr += (I*C)**2
                Retrieved_list[doc] = score,LDsqr
            else:
                score,LDsqr = Retrieved_list[doc]
                score += W* I * C
                LDsqr += (I*C)**2
                Retrieved_list[doc] = score,LDsqr
        

L = math.sqrt(LQsqr)
    
for each in Retrieved_list:
    score,LDsqr = Retrieved_list[each]
    score = score/(L*math.sqrt(LDsqr))
    Retrieved_list[each] = score
    
# sort the document by score
sorted_Retrieved_list = OrderedDict(sorted(Retrieved_list.items(),key=lambda x: x[1],reverse = True))


for D in sorted_Retrieved_list:
    file  = open("processedFiles/"+D,'r')
    for i in range(1):
        url =file.readline()
        print(url)
        print('\n')
    file.close()


