import os
import cloudscraper
import sys, threading
import urllib.request
from bs4 import BeautifulSoup
import mysql.connector
from html import unescape

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="thiet"
)

# with open("copy.html", "w", encoding="utf-8") as f:
    # f.write(str(scraper.get("https://metruyenchu.com/truyen/vu-than-chua-te/chuong-1").text))

sys.setrecursionlimit(10**7) # max depth of recursion
threading.stack_size(2**27)  # new thread will get stack of such size

scraper = cloudscraper.create_scraper(
 	browser={
    	'browser': 'firefox',
    	'platform': 'windows',
    	'mobile': False
    }
)

mycursor = mydb.cursor()

selectDauThau = "SELECT link_detail FROM `dau_thaus` WHERE status = 1 limit 1";
mycursor.execute(selectDauThau)

myresult = mycursor.fetchall()

link = '';
for x in myresult:
	link = x[0]

print(link)
html = scraper.get(link)

source_code = str(html.text)
soup = BeautifulSoup(source_code, 'html.parser')
content = soup.findChildren('table',{'class':'t-tbl-detail'})

def html_decode(s):
    """
    Returns the ASCII decoded version of the given HTML string. This does
    NOT remove normal HTML tags like <p>.
    """
    htmlCodes = (
            ("'", '&#39;'),
            ('"', '&quot;'),
            ('>', '&gt;'),
            ('<', '&lt;'),
            ('&', '&amp;')
        )
    for code in htmlCodes:
        s = s.replace(code[1], code[0])
    return s

if(content):
	count = 0;
	mysql = 'UPDATE dau_thaus SET '
	mysql1 = mysql2 = mysql3 = mysql4 = mysql5 = ''
	for child in content:
		if(count == 0):
			mysql1 = "info1 = '"+html_decode(str(child))+"', "
		if(count == 1):
			mysql2 = "info2 = '"+html_decode(str(child))+"', "
		if(count == 2):
			mysql3 = "info3 = '"+html_decode(str(child))+"', "
		if(count == 3):
			mysql4 = "info4 = '"+html_decode(str(child))+"', status = 2 "
		count = count + 1
	mysql5 = " WHERE link_detail = '" + link + "'"
	if(mysql1 == '' or mysql2 == '' or mysql3 == '' or mysql4 == '' or mysql5 == ''):
		mysql = 'UPDATE dau_thaus SET status = -2 WHERE link_detail = "' + link + '"'
		mycursor.execute(mysql)
		mydb.commit()
	else:
		mysqlAll = mysql + mysql1 + mysql2 + mysql3 + mysql4 + mysql5
		mycursor.execute(mysqlAll)
		mydb.commit()
	