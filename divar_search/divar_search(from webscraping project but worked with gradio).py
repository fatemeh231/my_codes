import gradio as gr
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
import pandas as pd
import time
service = Service(r"C:\Users\fatemeh\OneDrive\Desktop\extra\geckodriver.exe")
options = Options()
options.binary_location = r"C:\Users\fatemeh\AppData\Local\Mozilla Firefox\firefox.exe"

def scrape_divar(search_term):
    driver = webdriver.Firefox(service=service, options=options)
    driver.get("https://divar.ir/s/tehran")
    time.sleep(5)

    # Search
    search_box = driver.find_element(By.XPATH, '/html/body/div[1]/header/nav/div[2]/div[2]/div/div/div[1]/form/input')
    search_box.click()
    search_box.send_keys(search_term + Keys.ENTER)
    time.sleep(5)

    # Data
    titles = [t.text for t in driver.find_elements(By.XPATH, "//h2[contains(@class,'kt-post-card__title')]")[:20]]
    prices = [p.text for p in driver.find_elements(By.XPATH, "//div[contains(@class,'kt-post-card__description')]") if "تومان" in p.text][:20]
    owners = [o.text for o in driver.find_elements(By.XPATH, "//span[contains(@class,'kt-post-card__bottom-description')]")[:20]]
    urls = [u.get_attribute("href") for u in driver.find_elements(By.XPATH, "//a[contains(@class,'kt-post-card')]")[:20]]

    driver.quit()

    # DataFrame
    min_len = min(len(titles), len(prices), len(owners), len(urls))
    df = pd.DataFrame({
        'property': titles[:min_len],
        'price': prices[:min_len],
        'owner': owners[:min_len],
        'url': urls[:min_len]
    })

    # Create HTML table with clickable links
    html_table = "<table border='1' style='border-collapse:collapse'><tr><th>Property</th><th>Price</th><th>Owner</th><th>URL</th></tr>"
    for i in range(min_len):
        html_table += f"<tr><td>{titles[i]}</td><td>{prices[i]}</td><td>{owners[i]}</td><td><a href='{urls[i]}' target='_blank'>لینک</a></td></tr>"
    html_table += "</table>"

    return html_table

# Gradio
gr.Interface(
    fn=scrape_divar,
    inputs=gr.Textbox(label="جستجو در دیوار", placeholder="مثلاً دوچرخه، لباسشویی، خانه..."),
    outputs=gr.HTML(label="نتایج جستجو")
).launch()