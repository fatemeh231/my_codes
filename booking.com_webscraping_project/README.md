# 🏨 Booking.com Hotel Scraper

## 📌 Overview
This project automates hotel searches on [Booking.com](https://www.booking.com) using **Selenium WebDriver** with Firefox.  
It allows the user to perform their **own search** (destination, dates, stay duration) and then scrapes hotel names, review scores, and review counts. The results are exported into an **Excel file** for easy analysis.

This script is designed for:
- Learning how to automate browser interactions with Selenium
- Collecting structured data from dynamic websites
- Practicing data cleaning and exporting with **Pandas**


## ⚙️ Requirements

### Software
- Python 3.8+
- Mozilla Firefox browser
- Geckodriver (compatible with your Firefox version)

### Python Libraries
Install the required packages:
```bash
pip install selenium beautifulsoup4 pandas openpyxl
```


## 📂 Project Structure
```
BookingScraper/
│
├── scraper.py                         # Main script
├── Tokyo_hotels_1month_october.xlsx   # Example output file
└── README.md                          # Documentation
```


## 🚀 How It Works
1. Launches Firefox via Selenium and opens Booking.com.
2. User enters their **own search criteria** (e.g., "Tokyo", flexible dates, stay length).
3. Script interacts with the site:
   - Submits the search
   - Selects flexible dates
   - Extracts hotel names, scores, and review counts
4. Cleans the data:
   - Normalizes review counts using regex
   - Fills missing scores with `"N/A"`
5. Saves results into an Excel file (`Tokyo_hotels_1month_october.xlsx`).

⚠️ **Important:** The data is dynamic and depends entirely on the search performed by the user at runtime.


## 📊 Example Output
The generated Excel file will look like:

| Hotel Name          | Score Text          | Review Count |
|---------------------|---------------------|--------------|
| Shinjuku Grand Inn  | 8.7 (123 reviews)   | 123          |
| Tokyo Central Hotel | N/A                 | 0            |


## 🛠️ Setup Instructions
1. Download and install [Firefox](https://www.mozilla.org/firefox/).
2. Download [Geckodriver](https://github.com/mozilla/geckodriver/releases) and place it in a known directory.
3. Update the script paths:
   - `service = Service(r"C:\path\to\geckodriver.exe")`
   - `options.binary_location = r"C:\path\to\firefox.exe"`
4. Run the script:
   ```bash
   python scraper.py
   ```


## ⚠️ Notes & Limitations
- **Website changes:** Booking.com frequently updates its HTML structure. If the script breaks, update the **XPath** or **CSS selectors**.
- **Waiting strategy:** The script currently uses `time.sleep()`. For more reliable automation, replace with `WebDriverWait`.
- **Ethical use:** This script is for **educational purposes only**. Always respect the website’s terms of service when scraping.


## 🔮 Future Improvements
- Add command-line arguments for city and date range (instead of hardcoding).
- Implement dynamic waits with `WebDriverWait`.
- Scrape additional hotel details (price, location, amenities).
- Support multiple destinations and export formats (CSV, JSON).


## 👩‍💻 Author
Created for educational and research purposes.  
Feel free to fork, adapt, and improve.