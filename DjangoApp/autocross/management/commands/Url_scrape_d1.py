from bs4 import BeautifulSoup
import requests
import mechanicalsoup
import sys
import datefinder
import dateparser
from dateutil import parser

sys.tracebacklimit = 0


browser = mechanicalsoup.StatefulBrowser()
URL = "https://mbasic.facebook.com/ccsportscarclub?v=events&is_past=1&serialized_cursor=AQHRhRfP4gYMJhCT0lkzk3AmMaQD5cr-0kXlexqw0-2SgoODFiZsuQAKtDbiPiGnT46jd7YrsjxjJkQgLPIdxIvjYg&has_more=1&refid=17"
browser.open(URL)



page = browser.get_current_page().find_all('div', class_='be')


for loc_data in page:
 # print(loc_data.text)
  location_list = {'Rantoul':'Rantoul, IL', 'Urbana':'Urbana, IL','Mahomet':'Mahomet, IL','Champaign':'Champaign, IL'}
  location = ""
  dates = datefinder.find_dates(loc_data.text, strict = False)
  for key,value in location_list.items():
    if loc_data.text.find(key) != -1:
      location = value
      print(location)

  x = loc_data.text
  print(x.replace('View Event Details', ''))


  print ("-----------------------")
  #matches =  datefinder.find_dates(x)
  #for match in matches:
   # print(match)  
  #print("---------------------------")
 # f = open("FBoutput.txt","a")
  #f.write(x.text + '\n')
  #f.close()""

  
while True:
  if browser.follow_link(text = "See More Events"):
    browser.get_url()
    page = browser.get_current_page().find_all('span', class_='bi')
    for loc_data in page:
      location_list = {'Rantoul':'Rantoul, IL', 'Urbana':'Urbana, IL','Mahomet':'Mahomet, IL','Champaign':'Champaign, IL'}
      location = ""
      dates = datefinder.find_dates(loc_data.text, strict = True)
      for key,value in location_list.items():
        if loc_data.text.find(key) != -1:
          location = value
          print(location)
          

      a = loc_data.text
      print(a.replace('View Event Details',''))
      
      print('----------------------')

          #for x in page:
           # f = open("FBoutput.txt", "a")
            #f.write(x.text + '\n')
            #f.close()
 

