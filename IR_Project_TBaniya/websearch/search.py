from nltk.stem import PorterStemmer


from websearch.indexer import *

from websearch.retriever import *
import socket

def preprocessquery(query):
    key_words = []
    querylist =[]
    querylist = query.strip().split(" ")
    stemmer = PorterStemmer()
    for each_word in querylist:
        each_word = stemmer.stem(each_word).lower()
        key_words.append(each_word)
    return key_words


'''create inverted index'''

print("Creating index")
filepath = "../processedFiles/"
index_Hash = makeIndex(filepath)

'''listen to a TCP port for query'''

try:
    print("Opening socket")
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.bind(('localhost', 8089))
    serversocket.listen(5) # become a server socket, maximum 5 connections
    print("Waiting for client")
    buffersize = 1000
    while True:
        connection, address = serversocket.accept()
        result = ""
        query = connection.recv(buffersize)

        print("Query: ", query.decode())
        querylist = preprocessquery(query.decode())

        print("connected", querylist)
        result = retriveweb(index_Hash,querylist).encode()
        #result = "this is test result. please comment or remove this after completing testing".encode()
        #resultsize = str(len(result))
        #print(resultsize)
        connection.send(result)

        connection.close()
except Exception as e:
    print("Exception occured: ", e)








