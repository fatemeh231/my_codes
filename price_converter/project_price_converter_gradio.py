import gradio as gr
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
import time

fiat = ["USD", "GBP", "EUR", "CAD", "TRY", "JPY", "NZD", "AUD", "AED", "SAR", "KWD", "QAR", "CNH"]
crypto = ["BTC", "ETH", "BNB", "SOL", "XRP", "ADA", "DOGE", "DOT", "AVAX", "LINK", "MATIC", "TON", "SHIB"]
stock = ["TSLA", "AMZN", "AAPL", "NFLX", "MSFT", "NVDA", "GOOGLE", "META"]
commodities = ["OIL", "GAS", "GOLD", "SILVER", "COPPER"]
all_symbols = fiat + crypto + stock + commodities

descriptions = {
    "USD": "US Dollar – world's primary reserve currency.",
    "GBP": "British Pound – oldest active currency, used in the UK.",
    "EUR": "Euro – official currency of the Eurozone.",
    "CAD": "Canadian Dollar – Canada's national currency.",
    "TRY": "Turkish Lira – currency of Turkey.",
    "JPY": "Japanese Yen – third most traded currency globally.",
    "NZD": "New Zealand Dollar – currency of New Zealand.",
    "AUD": "Australian Dollar – used in Australia and nearby islands.",
    "AED": "UAE Dirham – currency of the United Arab Emirates.",
    "SAR": "Saudi Riyal – currency of Saudi Arabia.",
    "KWD": "Kuwaiti Dinar – highest-valued currency unit globally.",
    "QAR": "Qatari Riyal – currency of Qatar.",
    "CNH": "Chinese Yuan – offshore version of China's currency.",
    "BTC": "Bitcoin – first and most valuable cryptocurrency.",
    "ETH": "Ethereum – smart contract platform and crypto asset.",
    "BNB": "Binance Coin – used in Binance ecosystem.",
    "SOL": "Solana – fast blockchain for decentralized apps.",
    "XRP": "Ripple – crypto for cross-border payments.",
    "ADA": "Cardano – blockchain focused on sustainability.",
    "DOGE": "Dogecoin – meme-based cryptocurrency.",
    "DOT": "Polkadot – connects multiple blockchains.",
    "AVAX": "Avalanche – scalable smart contract platform.",
    "LINK": "Chainlink – decentralized oracle network.",
    "MATIC": "Polygon – Ethereum scaling solution.",
    "TON": "Toncoin – Telegram-linked blockchain.",
    "SHIB": "Shiba Inu – meme coin with DeFi ambitions.",
    "TSLA": "Tesla – electric vehicle and energy company.",
    "AMZN": "Amazon – global e-commerce and cloud giant.",
    "AAPL": "Apple – consumer tech and innovation leader.",
    "NFLX": "Netflix – streaming entertainment platform.",
    "MSFT": "Microsoft – software and cloud computing giant.",
    "NVDA": "Nvidia – leader in AI and graphics chips.",
    "GOOGLE": "Google (Alphabet) – search and AI powerhouse.",
    "META": "Meta – social media and metaverse company.",
    "OIL": "Crude Oil – most traded global commodity.",
    "GAS": "Natural Gas – key energy source worldwide.",
    "GOLD": "Gold – traditional store of value and hedge.",
    "SILVER": "Silver – used in electronics and jewelry.",
    "COPPER": "Copper – essential for wiring and green tech."
}

def show_description(symbol):
    return descriptions.get(symbol, "No description available.")

def convert_to_rial(symbol):
    service = Service(r"C:\Users\fatemeh\OneDrive\Desktop\extra\geckodriver.exe")
    options = Options()
    options.binary_location = r"C:\Users\fatemeh\AppData\Local\Mozilla Firefox\firefox.exe"
    driver = webdriver.Firefox(service=service, options=options)

    if symbol in fiat:
        yahoo_url = f"https://finance.yahoo.com/quote/{symbol}=X/"
        driver.get(yahoo_url)
        time.sleep(5)
        price_element = driver.find_element(By.XPATH, '/html/body/div[2]/main/section/section/section/section/section[1]/div[2]/div[1]/section/div/section/div[1]')
        price_text = price_element.text.split("\n")[0].strip().replace(",", "")
        price_value = float(price_text)
        driver.get("https://alanchand.com/en/currencies-price/usd#calculator")
        time.sleep(5)
        rial_element = driver.find_element(By.XPATH, "/html/body/main/section[4]/div/div[2]/div/div[2]/div/input")
        rial_text = rial_element.get_attribute("value").replace(",", "")
        rial_value = float(rial_text)
        converted_value = rial_value / price_value

    elif symbol in crypto or symbol in stock:
        yahoo_url = f"https://finance.yahoo.com/quote/{symbol}-USD/" if symbol in crypto else f"https://finance.yahoo.com/quote/{symbol}/"
        driver.get(yahoo_url)
        time.sleep(5)
        price_element = driver.find_element(By.XPATH, '/html/body/div[2]/main/section/section/section/section/section[1]/div[2]/div[1]/section/div/section/div[1]')
        price_text = price_element.text.split("\n")[0].strip().replace(",", "")
        price_value = float(price_text)
        driver.get("https://alanchand.com/en/currencies-price/usd#calculator")
        time.sleep(5)
        rial_element = driver.find_element(By.XPATH, "/html/body/main/section[4]/div/div[2]/div/div[2]/div/input")
        rial_text = rial_element.get_attribute("value").replace(",", "")
        rial_value = float(rial_text)
        converted_value = rial_value * price_value

    elif symbol == "GOLD":
        yahoo_url = "https://finance.yahoo.com/quote/GC%3DF/"
    elif symbol == "OIL":
        yahoo_url = "https://finance.yahoo.com/quote/CL%3DF/"
    elif symbol == "SILVER":
        yahoo_url = "https://finance.yahoo.com/quote/SI%3DF/"
    elif symbol == "COPPER":
        yahoo_url = "https://finance.yahoo.com/quote/HG%3DF/"
    elif symbol == "GAS":
        yahoo_url = "https://finance.yahoo.com/quote/NG%3DF/"
    else:
        driver.quit()
        return "Invalid symbol"

    if symbol in commodities:
        driver.get(yahoo_url)
        time.sleep(5)
        price_element = driver.find_element(By.XPATH, '/html/body/div[2]/main/section/section/section/section/section[1]/div[2]/div[1]/section/div/section/div[1]')
        price_text = price_element.text.split("\n")[0].strip().replace(",", "")
        price_value = float(price_text)
        driver.get("https://alanchand.com/en/currencies-price/usd#calculator")
        time.sleep(5)
        rial_element = driver.find_element(By.XPATH, "/html/body/main/section[4]/div/div[2]/div/div[2]/div/input")
        rial_text = rial_element.get_attribute("value").replace(",", "")
        rial_value = float(rial_text)
        converted_value = rial_value * price_value

    driver.quit()
    return f"{symbol} to IRR: {converted_value:,.2f} Rials"

with gr.Blocks() as demo:
    gr.Markdown("## 💱 Currency/Asset to Rial Converter")
    gr.Markdown("Select a symbol to preview its description and convert its value to Iranian Rials.")

    with gr.Row():
        symbol_dropdown = gr.Dropdown(choices=all_symbols, label="Choose a symbol", interactive=True)
        description_box = gr.Textbox(label="Description", interactive=False)

    symbol_dropdown.change(fn=show_description, inputs=symbol_dropdown, outputs=description_box)

    convert_button = gr.Button("Convert to Rial")
    result_box = gr.Textbox(label="Converted Value", interactive=False)

    convert_button.click(fn=convert_to_rial, inputs=symbol_dropdown, outputs=result_box)

demo.launch(share=True)
