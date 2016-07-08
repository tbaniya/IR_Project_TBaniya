#!/Python34/python
import math
#from nltk.stem import PorterStemmer
from collections import OrderedDict


def retriveweb(index_Hash,key_words):
    Retrieved_list = {}
    count = 500
    LQsqr = 0.0
    L = 0.0
    LDsqr = 0.0
    #stemmer = PorterStemmer()

    for each_token in key_words:
        #each_token = stemmer.stem(each_token).lower()
        if each_token in index_Hash:
            doc_hash = {}
            doc_hash = index_Hash[each_token]
            K = key_words.count(each_token)
            m = len(doc_hash)
            I = math.log2(count/m)
            #print(K,m,I)
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

    count = 0
    result = ""
    if len(Retrieved_list) == 0:
        result += "<p>"+ str(count) + " Total Number of Pages Retrieved :</p>\n"
        return result
        #print("Sorry no doucument found")

        
    else:
        for each in Retrieved_list:
            score,LDsqr = Retrieved_list[each]
            score = score/(L*math.sqrt(LDsqr))
            Retrieved_list[each] = score
           
        # sort the document by score
        sorted_Retrieved_list = OrderedDict(sorted(Retrieved_list.items(),key=lambda x: x[1],reverse = True))
        
        result += "<p>"+str(len(sorted_Retrieved_list))+" Total Number of Pages Retrieved :</p>\n"
        for D in sorted_Retrieved_list:
            count +=1
            file  = open("../processedFiles/"+D,'r')
            for i in range(1):
                url =file.readline().strip("\n")
                result += '<p>' + str(count) + '. <a href="'+url+'" target="new">'+url+'</a></p>\n'


            file.close()
        #print(result)
        return result

