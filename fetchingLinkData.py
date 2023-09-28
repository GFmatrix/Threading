import threading
import time
import json
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

def load(filename):
  with open(filename, "r", encoding='utf-8') as f:
    return json.load(f)

def dump(filename, data):
  with open(filename, "w") as f:
    json.dump(data, f)

def get_data(driver, link, key):
  driver.get(link)
  driver.maximize_window()
  wait = WebDriverWait(driver, 30)
  wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#mainContent > div:nth-child(2) > div:nth-child(3) > div:nth-child(2) > div:nth-child(1)")))

  time.sleep(5)

  html = driver.page_source

  soup = BeautifulSoup(html, features="lxml")
  aside = soup.find('div', attrs={"data-testid": "aside"})
  name = aside.find('h1', attrs={"data-cy": "ad_title"}).text.strip() 
  price = aside.find('div', attrs={"data-testid": "ad-price-container"}).text.strip() 
  location = aside.select_one('div:nth-child(3)').text.strip()
  main_ = soup.find('div', attrs={"data-testid": "main"})
  description = main_.find('div', attrs={"data-cy": "ad_description"}).text.strip()
  return {"name": name, "price": price, "location": location, "description": description}

def main(link_list, filename):
  chrome_options = Options()
  chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36")
  print(f"Starting Thread {threading.current_thread().name}")
  driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
  data = []
  for key, link in enumerate(link_list):
    try:
      data.append(get_data(driver, link, key))
    except Exception as e:
      print(e)
      continue
  
  dump(filename, data)
    
  driver.close()
  print(f"Finishing Thread {threading.current_thread().name}")
  
if __name__ == "__main__":
  linkList = load("links.json")
  for i in range(4):
    a = linkList[len(linkList) // 4 * i:len(linkList) // 4 * (i + 1)]
    x = threading.Thread(target=main, args=(a, f'data/dataN{i}.json', ), name=i)
    x.start()