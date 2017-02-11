# import sys
#
# from PySide.QtWebKit import QWebView
# from PySide.QtGui import QApplication
# from PySide.QtCore import QUrl
#
# app = QApplication(sys.argv)
#
# browser = QWebView()
# browser.load(QUrl('https://clients.mindbodyonline.com/launch'))
# browser.show()
#
# app.exec_()


import sys
from PySide.QtCore import *
from PySide.QtGui import *
from PySide.QtWebKit import *
from PySide.QtNetwork import *

class XPrinter(QObject):

    def __init__(self):
        QObject.__init__(self)

    def print_page_info(self, ok):
        print "Finished", ok

    def print_load_started(self):
        print 'started loading'

    def print_load_percent(self, percent):
        print percent

    def onFrame(self, val):
        print 'Frame Created:', val.frameName()


app = QApplication(sys.argv)

web = QWebView()
xprinter = XPrinter()
web.loadFinished.connect(xprinter.print_page_info)
web.loadStarted.connect(xprinter.print_load_started)
web.loadProgress.connect(xprinter.print_load_percent)
web.page().frameCreated.connect(xprinter.onFrame)

web.load(QUrl("https://clients.mindbodyonline.com/launch"))
# web.setWindowState(Qt.WindowMaximized)
web.show()

sys.exit(app.exec_())
