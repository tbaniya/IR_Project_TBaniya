'''This code is for testin purpose for passing query to the search engine
from python code without using browser.
Deleting this file will not harm the project. However be kind to keep this file.
'''

import socket
result = ""
clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

query = "vasile rus"
clientsocket.connect(('localhost', 8089))
clientsocket.sendall(query.encode())
buffsize = 10
data = clientsocket.recv(buffsize).decode()
result = ""
while data:
    result += data
    data = clientsocket.recv(buffsize).decode()

print(result)
clientsocket.close()




#buff = clientsocket.recv(64)
#print(buff.decode())
