# -*- coding:utf-8 -*-
import os
import sys
import http.client
import urllib.request
from xml.dom.minidom import parseString

client_id = "3xrQhsEXks_VPCP_OdoJ"
client_secret = "WTsm8rKIH4"

conn = http.client.HTTPSConnection("openapi.naver.com")
headers = {"X-Naver-Client-Id": client_id, "X-Naver-Client-Secret": client_secret}
# encText = "love"
encText = urllib.parse.quote('그리고 아무도 없었다')
params = "?query=" + encText + "&display=2&start=1"

# isbn = '9780596513986' #Learning Python 3(E) isbn
# params = "?d_isbn=" + isbn
conn.request("GET", "/v1/search/book.xml" + params, None, headers)
# conn.request("GET", "/v1/search/book_adv.xml" + params, None, headers)
res = conn.getresponse()

if int(res.status) == 200 :
    print(parseString(res.read().decode('utf-8')).toprettyxml())
else:
    print ("HTTP Request is failed :" + res.reason)
    print (res.read().decode('utf-8'))

conn.close()