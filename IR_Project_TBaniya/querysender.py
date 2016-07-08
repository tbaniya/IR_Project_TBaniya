#!/Python34/python
import cgi
import os
import socket
os.environ.__setitem__('APPDATA','C:\Python34\Lib\site-packages')
form = cgi.FieldStorage()                 # parse form data
print('Content-type: text/html\n')        # hdr plus blank line
print('<title>Reply Page</title>')        # html reply page

result = ""
clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
if not 'key_word' in form:
    result += '<p><h1>Enter the word to search?</h1></p>'
    #print('<h1>Enter the word to search?</h1>')
else:
    #print('<h1>word you enter : <i>%s</i>!</h1>' % cgi.escape(form['key_word'].value))
    query = cgi.escape(form['key_word'].value)
    clientsocket.connect(('localhost', 8089))
    clientsocket.sendall(query.encode())
    buffsize = 1000

    data = clientsocket.recv(buffsize).decode()
    result = ""
    while data:
        result += data
        data = clientsocket.recv(buffsize).decode()

    print(result)

clientsocket.close()
