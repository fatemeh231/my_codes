📘 README – Currency/Asset to Rial Converter
📌 Overview
This project is an interactive Gradio app that lets users select a currency, cryptocurrency, stock, or commodity and instantly convert its value into Iranian Rials (IRR).
It combines:
• 	🌐 Yahoo Finance for live market data
• 	💱 AlanChand for USD-to-Rial conversion
• 	🐍 Python + Selenium for web automation
• 	🎨 Gradio for a clean, interactive user interface
Users can:
• 	Select a symbol (e.g., , , , )
• 	Preview its description
• 	Convert its live value into Rials

⚙️ Requirements
Software
• 	Python 3.8+
• 	Mozilla Firefox browser
• 	Geckodriver (compatible with your Firefox version)
Python Libraries
This project uses the following libraries:
• 	gradio → interactive web interface
• 	selenium → browser automation and scraping
• 	time → manage delays between actions

🚀 How to Run
1. 	Install requirements.
2. 	Download Geckodriver and set its path in the script.
3. 	Update Firefox binary path in the script if needed.
4. 	Run
5. 	A Gradio interface will launch in your browser.
6. 	Select a symbol → view description → click Convert to Rial → see the converted value