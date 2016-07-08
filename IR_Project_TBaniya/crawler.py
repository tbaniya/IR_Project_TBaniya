from bs4 import BeautifulSoup

from logger import writelog
from pdfreaderwriter import *
import os

count = 1


def readContent(url):
    global count
    file = None
    filename = ""
    try:
        writelog("Reading content of: " + url)
        response = urlopen(url)
        data = response.read().decode("utf-8",errors='ignore')
        soup = BeautifulSoup(data)
        text = soup.get_text()
        name = url.split('//')[-1]
        n = name + str(count) + ".txt"
        filename = "collection/" + n.replace('/','')
        file = open(filename,'w')
        file.write(url)
        file.write('\n')
        file.write(text)
        file.flush()
        writelog("Successfully read: " + url)
        #file.close()
        count += 1
        #file_log.write("Successfully crawled")
        #file_log.write('\n')
        
    except Exception as e:
        writelog("Exception: readContent " + url + " " + str(e))
        if file != None:
            file.close()
            os.remove(filename)

        #print("Failed: permission denied or link not working ")
        pass
    finally:
        if file != None:
            file.close()

def normalizeurl(parent_url,url):
    url = url.split('#')[0]
    url = url.split('?')[0]
    #case 1: http://www.memphis.edu/cs           parent
    #case 2: http://www.memphis.edu              root
    #case 3: url = /classes/thisweek.php
    #case 4: url = semester/spring.php
    if url.startswith('www.')  or url.startswith('http://') or url.startswith('https://'):
        return url.strip()

    if not url.startswith('/'):
        url =parent_url.strip("/") + "/" + url.strip("/")
        return url
    rooturl = ""
    if '://' in url:
        temp = url.split("://")
        rooturl = temp[1].split("/")[0]
        rooturl = temp[0]+ "://" + rooturl
    else:
        rooturl = url.split("/")[0]

    rooturl = rooturl.strip("/") + "/" + url.strip("/")
    return rooturl

def isvalidurl(url):
    lurl = url.lower()
    if lurl.endswith(".zip") or lurl.endswith(".rpm") or lurl.endswith(".tar") or lurl.endswith(".iso") \
            or lurl.endswith(".jpg") or lurl.endswith(".jpeg") or lurl.endswith(".png") or lurl.endswith(".gif") \
            or lurl.endswith(".mpeg") or lurl.endswith(".mov") or lurl.endswith(".mp3") or lurl.endswith(".mp4") or lurl.endswith(".vid") \
            or lurl.endswith(".rar") or lurl.endswith(".exe") or lurl.endswith(".jar") or lurl.endswith(".js") or lurl.endswith(".css") or \
            lurl.endswith(".ppt") or lurl.endswith(".pptx") or lurl.endswith(".doc") or lurl.endswith(".docx") or \
            lurl.endswith(".xls") or lurl.endswith(".xlsx") or lurl.endswith(".wav") or lurl.endswith(".wm") or \
            lurl.endswith(".wma") or lurl.endswith(".wmv") or lurl.endswith(".asf") or lurl.endswith(".ps") or lurl.endswith(".msi"):
        return False

    if "mailto:" in url.lower() or "tel:" in url.lower():
        return False
    if '://' in url:
        temp = url.split("://")
        rooturl = temp[1].split("/")[0]
    else:
        rooturl = url.split("/")[0]

    if "memphis.edu" not in rooturl:
        return False

    return True

def retrivePage(url):
    url = url.strip("/")
    #file_log.write("now crawling" + url)
    if url.endswith('.pdf'):
        writelog("Reading content of: " + url)
        readpdffromweb(url)
        writelog("Successfully read: " + url)
        return []
    else:
        readContent(url)
        try:

            response = urlopen(url)
            writelog("retrievePage; Fetching urls from: " + url)
            data = response.read().decode("utf-8",errors="ignore")
            soup = BeautifulSoup(data)
            url_list = []
            visited[url] = 1
            soup.prettify()
            for anchor in soup.findAll('a', href=True):
                norm_url = normalizeurl(url,anchor['href'])
                if not isvalidurl(norm_url):#skip rest statements in the loop and continue to remaining iteration
                    continue

                if norm_url not in url_list and norm_url not in visited:
                    url_list.append(norm_url)


            writelog("retrievePage; Success fetching urls from: " + url)
            return url_list

        except Exception as e:
            writelog("Exception: retrievePage " + url + " " +  str(e))
            #file_log.write("failed: permission denied or link not working")
            #file_log.write("\n")
            return []

visited = {}
total_url_list = []
#main_url = "http://www.memphis.edu/"
main_url = "http://www.memphis.edu/cs/"
#main_url = "http://www.memphis.edu/admissions/pdfs/checklist-4.pdf"

total_url_list = retrivePage(main_url)

while len(total_url_list) > 0:
    for each in total_url_list:
        total_url_list.remove(each)
        if each not in visited:
            visited[each] = 1
            result = retrivePage(each)
            if(result):
                total_url_list += result
        
        #time.sleep(2)
