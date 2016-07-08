#!/Python34/python
import os

count = 0
index_Hash = {}
def makeIndex(filepath):
    global count,index_Hash
    filelist = os.listdir(filepath)
    for filename in filelist:
        #tmp_hash stores word type and frequency in each document
        tmp_hash = {}
        count += 1
        file = open(filepath + filename,'r')
        # the first line of each file store the link to page, escape that line
        for i in range(1):
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
                
    return index_Hash
   







    
