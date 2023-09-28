import time
import json
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


driver = webdriver.Chrome(
    service=ChromeService(ChromeDriverManager().install()),
    # options=Options()
  )

page = 2

linkList = []

loop = True

while loop:
  driver.get(f"https://m.olx.uz/elektronika/?page={page}")

  driver.maximize_window()

  wait = WebDriverWait(driver, 30)
  listDiv = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#mainContent > div:nth-child(2) > form > div:nth-child(5) > div > div > div:nth-child(2)")))

  time.sleep(1)

  html = driver.page_source

  soup = BeautifulSoup(html, features="lxml")
  listDiv = soup.find('div', attrs={"data-testid": "listing-grid"})
  listDiv = listDiv.find_all('div', attrs={"data-cy": "l-card"})
  
  for link in listDiv:
    if len(linkList) != 100:
      linkList.append(f"https://m.olx.uz{link.find('a').get('href')}")
    else: 
      with open('links.json', 'w', encoding='utf-8') as f:
        json.dump(linkList, f, ensure_ascii=False, indent=2)
        f.close()
      loop = False
      break
  
  page += 1
    
driver.close()
