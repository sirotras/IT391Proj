from bs4 import BeautifulSoup
import requests
import mechanicalsoup
import sys

sys.tracebacklimit = 0

browser = mechanicalsoup.StatefulBrowser()
URL = "https://mbasic.facebook.com/ccsportscarclub?v=events&is_past=1&refid=17"
browser.open(URL)

page = browser.get_current_page().find_all("div", class_="be")

for x in page:
    print(x.text)

browser.get_url()
print(browser.get_url())
print("-------------------------------------")
#print(page.get_text())
print("--------------------------------------")



#while True:
  #  if browser.follow_link(text = "See More Events"):
   #     browser.get_url()
    #    page = browser.get_current_page().find("div", class_="be")
     #   print(browser.get_url())
      #  print(page.get_text())
       # print("---------------------------------------")
        
    #else:
     #   break


