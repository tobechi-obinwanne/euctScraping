# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""



import json
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def get_download_url_selenium(trial_number):
    url = f"https://euclinicaltrials.eu/ctis-public/view/{trial_number}"

    # Correct Selenium 4 syntax: enable performance logging via ChromeOptions
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),
                              options=options)

    driver.get(url)
    time.sleep(5)  # allow time for the page to fully load

    # Click the download button
    button = driver.find_element(By.XPATH, "//button[contains(text(),'Download clinical trial')]")
    button.click()
    time.sleep(5)  # wait for request completion

    logs = driver.get_log('performance')

    download_url = None
    # Extract the AWS URL from network logs
    for entry in logs:
        log = json.loads(entry['message'])['message']
        if log['method'] == 'Network.responseReceived':
            response_url = log['params']['response']['url']
            if "ctis-publication-engine-ct-zip-prod.s3.eu-central-1.amazonaws.com" in response_url:
                if trial_number in response_url:
                    download_url = response_url
                    break

    driver.quit()
    return download_url

def download_file(download_url, filename):
    with requests.get(download_url, stream=True) as r:
        r.raise_for_status()
        with open(filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)

if __name__ == "__main__":
    trial_number = '2022-500137-89-00'
    output_file = f"{trial_number}.zip"

    print("Getting URL...")
    url = get_download_url_selenium(trial_number)
    if url:
        print(f"Download URL obtained: {url}")
        print("Downloading file...")
        download_file(url, output_file)
        print(f"Download complete: {output_file}")
    else:
        print("Failed to get download URL.")
        
import os

print("\nSaved to:", os.path.abspath(output_file))

