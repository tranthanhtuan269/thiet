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

i = 1
while i < 477:
	html = scraper.get("http://muasamcong.mpi.gov.vn/lua-chon-nha-thau?p_auth=QaoDMSJLRB&p_p_id=luachonnhathau_WAR_bidportlet&p_p_lifecycle=1&p_p_state=normal&p_p_mode=view&p_p_col_id=column-1&p_p_col_count=2&_luachonnhathau_WAR_bidportlet_denNgay=&_luachonnhathau_WAR_bidportlet_tuNgay=&_luachonnhathau_WAR_bidportlet_sapXep=DESC&_luachonnhathau_WAR_bidportlet_nguonVon=1&_luachonnhathau_WAR_bidportlet_hinhThuc=1&_luachonnhathau_WAR_bidportlet_displayItem=10&_luachonnhathau_WAR_bidportlet_chuDauTu=&_luachonnhathau_WAR_bidportlet_timKiemTheo=&_luachonnhathau_WAR_bidportlet_benMoiThau=&_luachonnhathau_WAR_bidportlet_time=-1&_luachonnhathau_WAR_bidportlet_currentPage2="+str(i)+"&_luachonnhathau_WAR_bidportlet_currentPage1=1&_luachonnhathau_WAR_bidportlet_loaiThongTin=3&_luachonnhathau_WAR_bidportlet_searchText=&_luachonnhathau_WAR_bidportlet_dongMo=0&_luachonnhathau_WAR_bidportlet_javax.portlet.action=list")
	source_code = str(html.text)
	soup = BeautifulSoup(source_code, 'html.parser')
	content = soup.find('div',{'id':'tab2'})
	if(content):
		child2 = content.findChildren("td" , {'class': 'h-tbl-border'})
		for child3 in child2:
			mysql = 'INSERT INTO `dau_thaus` (`link_detail`) VALUES ('
			big_item = child3.findChildren("p")
			for sm_item in big_item:
				if(sm_item.get('title', '') != ''):
					if(sm_item.find("a" , {'class': 'container-tittle'})):
						item = sm_item.find("a" , {'class': 'container-tittle'})
						mysql += '"'+item['href']+'"'
			mysql += ')'
			print(mysql)
			mycursor.execute(mysql)
			mydb.commit()
			print('--------------------------')
	i = i + 1