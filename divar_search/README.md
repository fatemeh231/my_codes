README – Divar Scraper with Gradio
📌 Overview
This project is a Python web scraper that uses Selenium to extract property listings from Divar.ir (Tehran section).
It fetches:
• 	🏠 Property titles
• 	💰 Prices (in تومان)
• 	👤 Owner information
• 	🔗 Direct clickable URLs
The results are displayed in a Gradio web interface, making it interactive and user-friendly.

⚙️ Requirements
Software
• 	Python 3.8+
• 	Mozilla Firefox browser
• 	Geckodriver (compatible with your Firefox version)
Python Libraries
This project uses the following libraries:
• 	gradio → to build the interactive web interface
• 	selenium → to automate browser actions and scrape data
• 	pandas → to structure scraped data into tables
• 	time → to manage delays between actions
• 	webdriver (selenium.webdriver) → Firefox driver, service, options, keys for automation

🚀 How to Run
1. 	Install requirements.
2. 	Download Geckodriver and set its path in the script.
3. 	Update Firefox binary path in the script if needed.
4. 	Run
5. 	A Gradio interface will launch in your browser.
6. 	Enter a search term (e.g., "دوچرخه", "خانه", "لباسشویی") and view results in a clickable HTML table