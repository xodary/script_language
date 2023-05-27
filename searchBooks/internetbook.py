# -*- coding:cp949 -*-
from xmlbook import *
import urllib.request
from http.client import HTTPSConnection
from http.server import BaseHTTPRequestHandler, HTTPServer

conn = None
client_id = "3xrQhsEXks_VPCP_OdoJ"
client_secret = "WTsm8rKIH4"

# ���̹� OpenAPI ���� ���� information
server = "openapi.naver.com"

# smtp ����
host = "smtp.gmail.com" # Gmail SMTP ���� �ּ�.
port = "587"

def userURIBuilder(uri, **user):
    str = uri + "?"
    for key in user.keys():
        str += key + "=" + user[key] + "&"
    return str

def connectOpenAPIServer():
    global conn, server
    conn = HTTPSConnection(server)
    conn.set_debuglevel(1)
        
def getBookDataFromTitle(str):
    global server, conn, client_ID, client_secret
    if conn == None :
        connectOpenAPIServer()
    encText = str
    if not encText.encode().isalpha():
        encText = urllib.parse.quote(encText)
    uri = userURIBuilder("/v1/search/book.xml", display="1", start="1", query=encText)
    conn.request("GET", uri, None, {"X-Naver-Client-Id": client_id, "X-Naver-Client-Secret": client_secret})
    
    req = conn.getresponse()
    print (req.status)
    if int(req.status) == 200 :
        print("Book data downloading complete!")
        return extractBookData(req.read())
    else:
        print ("OpenAPI request has been failed!! please retry")
        return None

def extractBookData(strXml):
    from xml.etree import ElementTree
    tree = ElementTree.fromstring(strXml)
    print (strXml)
    # Book ������Ʈ�� �����ɴϴ�.
    itemElements = tree.iter("item")  # return list type
    #itemElements = tree.getiterator("item")  # return list type
    print(itemElements)
    for item in itemElements:
        image = item.find("image")
        author = item.find("author")
        strTitle = item.find("title")
        discount = item.find("discount")
        publisher = item.find("publisher")
        description = item.find("description")
        print (strTitle)

        if len(strTitle.text) > 0 :
           return {"author":author.text,"title":strTitle.text, "image":image.text,
                   "discount":discount.text, "publisher": publisher.text, "description":description.text}

def sendMain():
    global host, port
    html = ""
    title = str(input ('Title :'))
    senderAddr = str(input ('sender email address :'))
    recipientAddr = str(input ('recipient email address :'))
    msgtext = str(input ('write message :'))
    passwd = str(input (' input your password of gmail account :'))
    msgtext = str(input ('Do you want to include book data (y/n):'))
    if msgtext == 'y' :
        keyword = str(input ('input keyword to search:'))
        html = MakeHtmlDoc(SearchBookTitle(keyword))
    
    import mysmtplib
    # MIMEMultipart�� MIME�� �����մϴ�.
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    
    #Message container�� �����մϴ�.
    msg = MIMEMultipart('alternative')

    #set message
    msg['Subject'] = title
    msg['From'] = senderAddr
    msg['To'] = recipientAddr
    
    msgPart = MIMEText(msgtext, 'plain')
    bookPart = MIMEText(html, 'html', _charset = 'UTF-8')
    
    # �޼����� ������ MIME ������ ÷���մϴ�.
    msg.attach(msgPart)
    msg.attach(bookPart)
    
    print ("connect smtp server ... ")
    s = mysmtplib.MySMTP(host,port)
    #s.set_debuglevel(1)
    s.ehlo()
    s.starttls()
    s.ehlo()
    s.login(senderAddr, passwd)    # �α��� �մϴ�. 
    s.sendmail(senderAddr , [recipientAddr], msg.as_string())
    s.close()
    
    print ("Mail sending complete!!!")

class MyHandler(BaseHTTPRequestHandler):
    
    def do_GET(self):
        from urllib.parse import urlparse
        import sys
      
        parts = urlparse(self.path)
        keyword, value = parts.query.split('=',1)

        if keyword == "title" :
            html = MakeHtmlDoc(SearchBookTitle(value)) # keyword�� �ش��ϴ� å�� �˻��ؼ� HTML�� ��ȯ�մϴ�.
            ##��� �κ��� �ۼ�.
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(html.encode('utf-8')) #  ����( body ) �κ��� ��� �մϴ�.
        else:
            self.send_error(400,' bad requst : please check the your url') # �� ���� ��û��� ������ �����Ѵ�.
        
def startWebService():
    try:
        server = HTTPServer( ('localhost',8080), MyHandler)
        print("started http server....")
        server.serve_forever()
        
    except KeyboardInterrupt:
        print ("shutdown web server")
        server.socket.close()  # server �����մϴ�.

def checkConnection():
    global conn
    if conn == None:
        print("Error : connection is fail")
        return False
    return True