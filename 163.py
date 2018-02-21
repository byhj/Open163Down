
import urllib.request
import bs4
import sys
import os

def getDownList(website, keyword):
    downList=[]
    html = urllib.request.urlopen(website).read()
    soup = bs4.BeautifulSoup(html, "html.parser")
    for line in soup.findAll("a") : #使用标签结构寻找
        if keyword in str(line):
            url = str(line["href"]).strip()
            downList.append(url)
    return downList

if __name__=="__main__" :
    website = str(sys.argv[1])     # get the download website
    keyword = "http://open.163.com/movie/"
    downList = getDownList(website, keyword)
    dirName = website[website.rfind("/")+1 : website.rfind(".")]
    targetPath = os.path.join(os.getcwd(), dirName)
    if not os.path.exists(targetPath):   #create the download dir according the course
        os.mkdir(targetPath)
    os.chdir(targetPath)

    cmd = "you-get %s"   #run the you-get to download the video
    for url in downList :
        os.system(cmd %url)


