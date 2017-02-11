import sys
import PySide.QtGui as QtGui
import PySide.QtCore as QtCore
import PySide.QtWebKit as QtWebKit

from lxml import html
import urllib2
from ntlm3 import HTTPNtlmAuthHandler

# Take this class for granted.Just use result of rendering.
class Render(QtWebKit.QWebPage):
    def __init__(self, url):
        self.app = QtGui.QApplication(sys.argv)
        QtWebKit.QWebPage.__init__(self)

        self.loadFinished.connect(self._loadFinished)
        self.networkAccessManager().finished.connect(self._finished)
        self.mainFrame().load(QtCore.QUrl(url))
        self.app.exec_()

    def _loadFinished(self, result):
        self.frame = self.mainFrame()
        self.app.quit()

    def _finished(self, reply):
        print reply.error()


# Take this class for granted.Just use result of rendering.
class Render2(QtWebKit.QWebPage):
    def __init__(self, url):
        user = 'Siteowner'
        password = 'apitest1234'
        passman = urllib2.HTTPPasswordMgrWithDefaultRealm()
        passman.add_password(None, url, user, password)
        auth_NTLM = HTTPNtlmAuthHandler.HTTPNtlmAuthHandler(passman)
        opener = urllib2.build_opener(auth_NTLM)
        opener.addheaders = [("X-FORMS_BASED_AUTH_ACCEPTED", "f")]
        urllib2.install_opener(opener)

        self.app = QtGui.QApplication(sys.argv)
        QtWebKit.QWebPage.__init__(self)
        self.connect(self.networkAccessManager(),
                     QtCore.SIGNAL("sslErrors (QNetworkReply *, const QList<QSslError> &)"),
                     self.sslErrorHandler)
        self.loadFinished.connect(self._loadFinished)
        self.mainFrame().load(QtCore.QUrl(url))
        self.app.exec_()


    def sslErrorHandler(self, reply, errorList):
        reply.ignoreSslErrors()
        print ("SSL error ignored")

    def _loadFinished(self, result):
        self.frame = self.mainFrame()
        self.app.quit()


if __name__ == "__main__":
    # url = 'http://pycoders.com/archive/'
    url = 'https://clients.mindbodyonline.com/classic/home?studioid=-99'
    r = Render(url)
    # result is a QString
    result = r.frame.toHtml()

    # QString should be converted to string before processed by lxml
    formatted_result = result.encode("utf-8")
    # Next build lxml tree from formatted_result
    tree = html.fromstring(formatted_result)
    # Now using correct Xpath we are fetching URL of archives
    archive_links = tree.xpath('//div[@class="campaign"]/a/@href')
    print archive_links