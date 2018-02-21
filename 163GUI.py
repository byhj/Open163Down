
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton,QLineEdit
from PyQt5.QtCore import QThread, QTime

import urllib.request
import bs4
import sys
import os
import time

def getDownList(website, keyword):
    downList=[]
    html = urllib.request.urlopen(website).read()
    soup = bs4.BeautifulSoup(html, "html.parser")
    for line in soup.findAll("a") :   #使用标签结构寻找下载链接
        if keyword in str(line):
            url = str(line["href"]).strip()
            downList.append(url)
    return downList

class DownThread(QThread):  #创建工作子线程防止主界面卡死
    def __init__(self, url):
        super().__init__()
        self.url = url

    def run(self):
        url = self.url
        if url != "":
            website = str(url)  # get the download website
            keyword = "http://open.163.com/movie/"
            downList = getDownList(website, keyword)
            dirName = website[website.rfind("/") + 1: website.rfind(".")]
            targetPath = os.path.join(os.getcwd(), dirName)
            if not os.path.exists(targetPath):  # create the download dir according the course
                os.mkdir(targetPath)

            os.chdir(targetPath)
            cmd = "you-get %s"  # run the you-get to download the video
            for url in downList:
                os.system(cmd % url)

class DownWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initGUI()

    def initGUI(self):
        self.resize(1000, 700)
        self.setWindowTitle("Open163Down")
        downBtn = QPushButton("下载", self)
        downBtn.setGeometry(200, 200, 200, 100)
        downBtn.clicked.connect(self.buttonClicked)
        quitBtn = QPushButton('退出', self)
        quitBtn.setGeometry(600, 200, 200, 100)
        quitBtn.clicked.connect(QApplication.instance().quit)

        self.urlLineEdit = QLineEdit(self)
        self.urlLineEdit.setText("http://open.163.com/special/innercore/")
        self.urlLineEdit.setGeometry(100, 100, 800, 60)
        self.show()

    def buttonClicked(self):
        self.downThread = DownThread(self.urlLineEdit.text())
        self.downThread.start()

if __name__=="__main__" :
    app = QApplication(sys.argv)
    w = DownWindow()
    sys.exit(app.exec_())

