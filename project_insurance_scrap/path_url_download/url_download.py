import urllib
import requests
#import charade
#charade.detect(response.content)['encoding']

def doc_download(url,file_name):
    try:
        u = urllib.request.urlopen(url)
    except urllib.error.HTTPError:
        return "fail " + file_name
    
    f = open(file_name, 'wb')
    block_sz = 8192
    while True:
        buffer = u.read(block_sz)
        if not buffer:
            break

        f.write(buffer)
    f.close()

def rar_download(url,file_name):   
    r=requests.get(url)
    
    with open(file_name,"w+b") as f:
        f.write(r.content)
    f.close()
    

