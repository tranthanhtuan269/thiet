import os
import cloudscraper
import sys, threading
import urllib.request
from bs4 import BeautifulSoup
import mysql.connector

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

html = scraper.get(link)
source_code = str(html.text)
soup = BeautifulSoup(source_code, 'html.parser')
content = soup.find('div',{'id':'tab2'})
if(content):
	child2 = content.findChildren("td" , {'class': 'h-tbl-border'})
	for child3 in child2:
		mysql = 'INSERT IGNORE INTO `dau_thaus` (`link_detail`, `tieu_de`, `mo_ta`, `vi_tri`,`uid`, `ngay_dang_tai`, `linh_vuc`, `status`) VALUES ('
		big_item = child3.findChildren("p")
		for sm_item in big_item:
			if(sm_item.get('title', '') != ''):
				if(sm_item.find("a" , {'class': 'container-tittle'})):
					item = sm_item.find("a" , {'class': 'container-tittle'})
					mysql += '"'+item['href']+'", '
				mysql += '"'+sm_item.get('title', 'No title attribute')+'", '
			else:
				sm_item.find("span", {'class', 'color-1'})
				mysql += '"'+sm_item.getText()+'", '
		# mysql = mysql[0:-2]
		mysql += '1)'
		print(mysql)
		mycursor.execute(mysql)
		mydb.commit()
		print('--------------------------')
