import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import os
import wget

# Download and set up Chrome WebDriver
def setup_chromedriver():
    chromedriver_path = '/mount/src/litscrape/chromedriver'  # Set the desired path on the server
    
    # Check if chromedriver already exists, if not, download it
    if not os.path.exists(chromedriver_path):
        os.makedirs('/mount/src/litscrape', exist_ok=True)
        chromedriver_url = "https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/116.0.5845.96/linux64/chromedriver-linux64.zip"
        zip_path = "/mount/src/litscrape/chromedriver.zip"  # Set the desired path on the server
        wget.download(chromedriver_url, zip_path)
        os.system(f"unzip {zip_path} -d {os.path.dirname(chromedriver_path)}")
        os.chmod(chromedriver_path, 0o775)
    
    return chromedriver_path

# Web scraping function using Selenium
def scrape_data(url):
    chromedriver_path = setup_chromedriver()
    
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.binary_location = '/usr/bin/google-chrome'  # Path to Chrome binary on the server
    
    service = Service(chromedriver_path)  # Set the path to Chrome WebDriver executable
    
    driver = webdriver.Chrome(service=service, options=options)
    
    driver.get(url)
    
    data = driver.find_element_by_xpath('/html/body/div/main/div[2]/div[2]/div[1]/h2/p').text
    # Scraping logic here
    
    driver.quit()
    return data

# Streamlit web app
def main():
    st.title('Web Scraping App')
    st.write("This app scrapes data from a website using Selenium.")
    
    url = "https://psyteam-fc61f.web.app/"  # URL to the website you want to scrape
    data = scrape_data(url)
    
    st.write("Scraped Data:")
    st.write(data)

if __name__ == '__main__':
    main()
