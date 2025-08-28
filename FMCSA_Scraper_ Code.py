import time
import os
import pandas as pd
import threading
import tkinter as tk
from tkinter import filedialog, messagebox
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager



def start_scraping(filename, mc_start, mc_end, status_label):
    try:
        # Prepare file path
        output_path = os.path.join(os.getcwd(), f"{filename}.xlsx")

        # Create dataframe
        columns = [
            'MC Number', 'Phone Number', 'Operating Authority',
            'Carrier Type', 'Trucks', 'USDOT Status',
            'Company Name', 'Physical Address', 'Drivers'
        ]
        data_frame = pd.DataFrame(columns=columns)
        invalid = 0
        i = 0

        # Start browser
        browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        wait = WebDriverWait(browser, 10)

        mc = mc_start
        while mc <= mc_end:
            mc += 1
            try:
                # Restart browser every 50 records
                if i % 50 == 0 and i != 0:
                    browser.quit()
                    browser = webdriver.Chrome()
                    wait = WebDriverWait(browser, 10)

                # Visit snapshot page
                browser.get("https://safer.fmcsa.dot.gov/CompanySnapshot.aspx")
                time.sleep(1)
                wait.until(EC.presence_of_element_located((By.ID, "2")))

                # Enter MC number
                browser.find_element(By.ID, "2").click()
                browser.find_element(By.ID, "4").clear()
                browser.find_element(By.ID, "4").send_keys(str(mc))
                browser.find_element(By.CSS_SELECTOR, "input[value='Search']").click()
                time.sleep(2)

                # Extract data
                wait.until(EC.presence_of_element_located((By.TAG_NAME, "table")))
                number = browser.find_element(By.CSS_SELECTOR,"table:nth-child(2) tr:nth-child(14) td:nth-child(2)").text.strip()
                authority = browser.find_element(By.CSS_SELECTOR,"table:nth-child(2) tr:nth-child(8) td:nth-child(2)").text.strip()
                trucks = browser.find_element(By.XPATH, "//tbody/tr[17]/td[1]").text.strip()
                carrier_or_broker = browser.find_element(By.CSS_SELECTOR,"body > p:nth-child(1) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(2) > td:nth-child(2) > table:nth-child(2) > tbody:nth-child(1) > tr:nth-child(2) > td:nth-child(1) > center:nth-child(3) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(3) > td:nth-child(2)").text
                usdot_status = browser.find_element(By.CSS_SELECTOR,"body > p:nth-child(1) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(2) > td:nth-child(2) > table:nth-child(2) > tbody:nth-child(1) > tr:nth-child(2) > td:nth-child(1) > center:nth-child(3) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(4) > td:nth-child(2)").text
                Comapny_name = browser.find_element(By.XPATH,"//body[1]/p[1]/table[1]/tbody[1]/tr[2]/td[1]/table[1]/tbody[1]/tr[2]/td[1]/center[1]/table[1]/tbody[1]/tr[11]/td[1]").text
                Physical_Adress = browser.find_element(By.XPATH, "//td[@id='physicaladdressvalue']").text
                Drivers = browser.find_element(By.XPATH,"//body[1]/p[1]/table[1]/tbody[1]/tr[2]/td[1]/table[1]/tbody[1]/tr[2]/td[1]/center[1]/table[1]/tbody[1]/tr[17]/td[2]/table[1]/tbody[1]/tr[1]/td[2]").text

                data_frame.loc[i] = [
                    mc, number, authority, carrier_or_broker,
                    trucks, usdot_status, Comapny_name, Physical_Adress, Drivers
                ]
                i += 1

            except Exception:
                invalid += 1
                continue

            # Update status in GUI
            status_label.config(text=f"Processing MC {mc}/{mc_end}... Saved: {i}, Skipped: {invalid}")
            status_label.update_idletasks()

        # Save Excel file
        data_frame.to_excel(output_path, index=False)
        browser.quit()

        status_label.config(text=f"✔️ Done! File saved: {output_path}")

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")


def run_scraper(filename_entry, mc_start_entry, mc_end_entry, status_label):
    filename = filename_entry.get().strip()
    if not filename:
        filename = "output_data"

    try:
        mc_start = int(mc_start_entry.get().strip())
        mc_end = int(mc_end_entry.get().strip())
    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid MC numbers")
        return

    # Run in a background thread so GUI doesn’t freeze
    threading.Thread(
        target=start_scraping,
        args=(filename, mc_start, mc_end, status_label),
        daemon=True
    ).start()


# ----------------- GUI -----------------
root = tk.Tk()
root.title("FMCSA Data Scraper")
root.geometry("450x300")

tk.Label(root, text="Excel Filename (without extension):").pack(pady=5)
filename_entry = tk.Entry(root, width=40)
filename_entry.pack()

tk.Label(root, text="Starting MC Number:").pack(pady=5)
mc_start_entry = tk.Entry(root, width=20)
mc_start_entry.pack()

tk.Label(root, text="Ending MC Number:").pack(pady=5)
mc_end_entry = tk.Entry(root, width=20)
mc_end_entry.pack()

status_label = tk.Label(root, text="Status: Waiting to start...", fg="blue")
status_label.pack(pady=10)

start_button = tk.Button(root, text="Start Scraping", command=lambda: run_scraper(filename_entry, mc_start_entry, mc_end_entry, status_label))
start_button.pack(pady=20)

root.mainloop()
