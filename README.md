# FMCSA Data Scraper

This is a Python-based GUI application that scrapes motor carrier data from the FMCSA (Federal Motor Carrier Safety Administration) company snapshot website. It extracts detailed company information for a range of MC (Motor Carrier) numbers and saves the results into an Excel file.

---

## Features

- Scrapes key data fields like Phone Number, Operating Authority, Carrier Type, Trucks, USDOT Status, Company Name, Physical Address, and Drivers.
- GUI interface built with Tkinter for easy input of MC number range and output filename.
- Automatically manages the Chrome WebDriver using `webdriver_manager`.
- Periodically restarts the browser session every 50 records to improve stability.
- Saves all scraped data in an Excel `.xlsx` file.
- Displays real-time status updates in the GUI during scraping.
- Runs the scraping process in a background thread to keep the GUI responsive.

---

## Requirements

- Python 3.7 or above
- Google Chrome browser installed
- The following Python packages:
  - `pandas`
  - `selenium`
  - `webdriver_manager`
  - `tkinter` (usually included with Python)
  
You can install required packages with pip:


---

## Usage

1. Run the script:
2. In the GUI window:
- Enter the desired Excel filename (without extension). Defaults to `output_data` if left blank.
- Enter the starting MC number.
- Enter the ending MC number.
- Click **Start Scraping** to begin.
3. The status label will update showing progress, saved records, and skipped entries.
4. Upon completion, the Excel file will be saved in the current working directory.

---

## Notes

- The program uses Selenium with Chrome WebDriver to automate browser interaction.
- Make sure Chrome is installed and up to date.
- The script handles intermittent failures by skipping invalid MC numbers and continuing.
- Large ranges may take time; the browser restarts every 50 records to reduce potential memory issues.
- The Excel file includes columns:

- MC Number
- Phone Number
- Operating Authority
- Carrier Type
- Trucks
- USDOT Status
- Company Name
- Physical Address
- Drivers

---

## Troubleshooting

- If the browser does not start, verify that Google Chrome is installed and accessible.
- Ensure that you have a stable internet connection as the tool fetches data from the FMCSA website.
- If the WebDriver fails, try updating the Chrome browser and rerun the script to allow `webdriver_manager` to update the driver.
- Permissions or firewall settings may block automated browser interactions—check security settings if issues arise.

---

## License

This project is open-source and free to use. No warranty is provided.

---

## Disclaimer

The data is scraped from the FMCSA official website for informational purposes only. Respect the terms of use of the FMCSA website when using this tool.
