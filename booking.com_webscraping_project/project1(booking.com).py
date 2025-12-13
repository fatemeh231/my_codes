from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
import time
from bs4 import BeautifulSoup
import pandas as pd
import re
service = Service(r"C:\Users\fatemeh\OneDrive\Desktop\extra\geckodriver.exe")
options = Options()
options.binary_location = r"C:\Users\fatemeh\AppData\Local\Mozilla Firefox\firefox.exe"
driver=webdriver.Firefox(service=service, options=options)
driver.get("https://www.booking.com/index.html?label=gen173nr-10CAEoggI46AdIM1gEaDuIAQGYATO4ARfIAQ_YAQPoAQH4AQGIAgGoAgG4AprI7ccGwAIB0gIkMmQ3OWFmNWEtMWZlMC00MDUyLWFkNTctNDAyMTg2ZjZjNTgw2AIB4AIB&aid=304142&sid=2c4dc14716e8bd5f82d81248fc6b1f21")

time.sleep(15)

link1= driver.find_element(By.XPATH,'//*[@id=":rh:"]')
link1.click()
link1.send_keys("tokyo")

time.sleep(5)

link2=driver.find_element(By.XPATH,'/html/body/div[3]/div[2]/div/form/div/div[4]/button')
link2.click()

time.sleep(10)

link3=driver.find_element(By.XPATH,'//*[@id="flexible-searchboxdatepicker-tab-trigger"]')
link3.click()
# //*[@id="flexible-searchboxdatepicker-tab-trigger"]flexible

time.sleep(2)

link4=driver.find_element(By.XPATH,'/html/body/div[4]/div/div/div/div[1]/div/form/div/div[2]/div/div/div/nav/div[3]/div/div[1]/div[1]/div/fieldset/div/div[3]')
link4.click()
#/html/body/div[4]/div/div/div/div[1]/div/form/div/div[2]/div/div/div/nav/div[3]/div/div[1]/div[1]/div/fieldset/div/div[2]/label/span[3]/div/how long want to stay

time.sleep(2)

link5=driver.find_element(By.XPATH,'/html/body/div[4]/div/div/div/div[1]/div/form/div/div[2]/div/div/div/nav/div[3]/div/div[1]/div[2]/div/fieldset/div/div[1]/div[1]/label/span')
link5.click()
# /html/body/div[4]/div/div/div/div[1]/div/form/div/div[2]/div/div/div/nav/div[3]/div/div[1]/div[2]/div/fieldset/div/div[1]/div[3]/label/span/when do you want to go

time.sleep(2)

link6=driver.find_element(By.XPATH,'/html/body/div[4]/div/div/div/div[1]/div/form/div/div[2]/div/div/div/nav/div[3]/div/div[2]/button')
link6.click()
# /html/body/div[4]/div/div/div/div[1]/div/form/div/div[2]/div/div/div/nav/div[3]/div/div[2]/button select dates

time.sleep(2)

link9=driver.find_element(By.XPATH,'/html/body/div[4]/div/div/div/div[1]/div/form/div/div[4]/button')
link9.click()
#search

time.sleep(10)

titles=driver.find_elements(By.CSS_SELECTOR,'[data-testid="title"]')
hotel_names=[title.text for title in titles]
    
scores = driver.find_elements(By.CSS_SELECTOR,'[data-testid="review-score"]')
hotel_scores = [score.text for score in scores]

while len(hotel_scores) < len(hotel_names):
    hotel_scores.append("N/A")

def extract_reviews(text):
    match = re.search(r'(\d[\d,]*) reviews', text)
    return int(match.group(1).replace(',', '')) if match else 0

review_counts = [extract_reviews(score) for score in hotel_scores]

# Create DataFrame
df = pd.DataFrame({
    "Hotel Name": hotel_names,
    "Score Text": hotel_scores,
    "Review Count": review_counts
})

print(df)

df.to_excel("Tokyo_hotels_1month_october.xlsx",index=False)

input("Press Enter to close the browser...")
driver.quit()

