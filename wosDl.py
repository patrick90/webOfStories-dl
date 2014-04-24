__author__ = 'hl'
from bs4 import BeautifulSoup
from urllib import urlopen
import re
import sys

def howManySubpages(masterWebpage):
    r=re.compile("activatePaginationLinks\(true, \d*, \d*\)")
    page= urlopen(masterWebpage).read()
    sa=re.findall(r, page)[0].split(',')[2]
    sa=sa[1:-1]
    return int(sa)

def extractTranscript(url):
    soup=BeautifulSoup(urlopen(url))
    transcript=str(soup.find(id="transcript-en"))
    title = str(soup.find("title"))
    title=title.replace("title", "h2")
    return title+transcript

def extractAllText(url):
    text=""
    title=url.split("/")[-2]
    myFile=codecs.open(title+".html", 'w')
    n=howManySubpages(url+"1")+1
    myFile.write('<head> <meta http-equiv="Content-Type" content="application/xhtml+xml; charset=utf-8" /> </head>')
    for i in range(1, n):
        myFile.write(extractTranscript(url+str(i)) )
        print("Percent " + str(float(i)/n))
    myFile.close()


def main():
    url = sys.argv[1]
    extractAllText(url)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nCTRL-C detected, shutting down....")
        sys.exit(0)
    except IndexError:
        print("You didn't specified url")
        sys.exit(0)