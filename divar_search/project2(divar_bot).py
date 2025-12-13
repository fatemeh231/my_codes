from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
import time
from bs4 import BeautifulSoup
import pandas as pd
import re
from selenium.webdriver.common.keys import Keys
service=Service(r"C:\Users\fatemeh\OneDrive\Desktop\extra\geckodriver.exe")
options=Options()
options.binary_location=r"C:\Users\fatemeh\AppData\Local\Mozilla Firefox\firefox.exe"
driver=webdriver.Firefox(service=service, options=options)
driver.get("https://divar.ir/s/tehran")

time.sleep(5)

seraching_item=input("لطفا دنبال ایتمی که می گردید را تایپ کنید.مانند دوچرخه،لباسشویی،خانه،گوشی و ...")
link1=driver.find_element(By.XPATH,'/html/body/div[1]/header/nav/div[2]/div[2]/div/div/div[1]/form/input')
link1.click()
link1.send_keys(seraching_item+Keys.ENTER)
#/html/body/div[1]/header/nav/div[2]/div[2]/div/div/div[1]/form/input (searching)

time.sleep(5)
# //h2[contains(@class, 'kt-post-card__title')] (title)
link2= driver.find_elements(By.XPATH,"//h2[contains(@class,'kt-post-card__title')]")
titles=[t.text for t in link2[:20]]
    
time.sleep(5)

# Find price
price1=driver.find_elements(By.XPATH, "//div[contains(@class,'kt-post-card__description')]")
prices=[p.text for p in price1 if "تومان" in p.text][:20]

time.sleep(5)

#get owner
owner1=driver.find_elements(By.XPATH,"//span[contains(@class,'kt-post-card__bottom-description')]")
owners=[o.text for o in owner1[:20]]

min_len=min(len(titles),len(prices),len(owners))
titles=titles[:min_len]
prices=prices[:min_len]
owners=owners[:min_len]

df=pd.DataFrame({
    'property':titles,
    'price':prices,
    'owner':owners})
print(df)
df.to_excel("divar_search.xlsx",index=False)

input("Press Enter to close the browser...")
driver.quit()

