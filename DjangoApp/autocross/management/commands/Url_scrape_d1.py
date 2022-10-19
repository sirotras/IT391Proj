from bs4 import BeautifulSoup
import requests
import mechanicalsoup
import sys
import datefinder

sys.tracebacklimit = 0

browser = mechanicalsoup.StatefulBrowser()
URL = "https://mbasic.facebook.com/ccsportscarclub?v=events&is_past=1&refid=17"
browser.open(URL)



page = browser.get_current_page().find_all('span', class_='bi')

for x in page:
  print(x.text)
  dates = datefinder.find_dates(x.text)
  location_list = {'Rantoul':'Rantoul, IL', 'Urbana':'Urbana, IL','Mahomet':'Mahomet, IL'}
  location = ""
  for key,value in location_list.items():
    if x.text.find(key) != -1:
      location = value
      print(location)
  
  

  for match in dates:
    print(match)
    
  print("---------------------------")
 # f = open("FBoutput.txt","a")
  #f.write(x.text + '\n')
  #f.close()

#browser.get_url()
#print(browser.get_url())
#print("-------------------------------------")


""" 
while True:
    if browser.follow_link(text = "See More Events"):
        browser.get_url()
        page = browser.get_current_page().find_all('span', class_='bi')
        for x in page:
          f = open("FBoutput.txt", "a")
          f.write(x.text + '\n')
          f.close()
 """


