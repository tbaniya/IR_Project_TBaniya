import os
import re
from PyPDF2 import PdfFileWriter, PdfFileReader
from urllib.request import urlopen
from logger import writelog

def readsavedpdf(path,link):
    file = None
    tfile = None
    try:
        file = open(path, "rb")
        path = path.replace('.pdf','')
        tfile = open(path +".txt",'w')
        reader = PdfFileReader(file)
        data = ""
        for i in range(0, reader.getNumPages()):
            data += reader.getPage(i).extractText() + "\n"
        #data = " ".join(data.replace(u"\xa0", " ").strip().split())
        data = " ".join(data.replace(u"\u02c7", " ").strip().split())
        tfile.write(link)
        tfile.write("\n")
        tfile.write(data)
        tfile.flush()

        #print("Successfully read pdf file")
    except Exception as e:
        writelog("Exception in reading: " + path + " " +str(e))
    finally:
        if file != None:
            file.close()
        if tfile != None:
            tfile.close()


def readpdffromweb(url):
    link = url
    tfile = None
    try:
        response = urlopen(url)
        tempfile = url.split('/')[-1]
        tfile = open("collection/"+tempfile, 'wb')
        tfile.write(response.read())
        
        tfile.flush()
        #tfile.close()
        
        readsavedpdf("collection/"+tempfile,link)
        tfile.close()
        #os.remove("collection/" + tempfile)
        #os.remove("collection/" + tempfile)
    except Exception as e:
        writelog("Exception in crawling: " + url + " " + str(e))
        #print("could not read ")
    finally:
        if tfile != None:
            if not tfile.closed:
                tfile.close()
            if tfile.closed:
                os.remove("collection/" + tempfile)
    

