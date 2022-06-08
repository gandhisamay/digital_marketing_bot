from bs4 import BeautifulSoup
from selenium import webdriver
import chromedriver_autoinstaller
import pandas as pd
from selenium.webdriver.common.by import By
from dotenv import load_dotenv

chromedriver_autoinstaller.install()

options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
options.add_argument('--headless')
driver = webdriver.Chrome(options=options)

print("Getting company data!")

company_websites = []
company_names = []
total_pages = 322

for i in range(0,total_pages-1):
    driver.get(f"https://clutch.co/us/agencies/digital?page={i}")

    page_source = driver.page_source

    soup = BeautifulSoup(page_source, 'lxml')

    company_info = soup.find_all('h3', class_ = 'company_info')


    for company in company_info:
        if company.find('a'):
            company_names.append(company.find('a').text.strip())

    company_web_a_list = soup.find_all('a', class_ = 'website-link__item')

    for company_web_a in company_web_a_list:
        if '?' in company_web_a['href']:
            company_websites.append(company_web_a['href'].rpartition('?')[0])
        else:
            company_websites.append(company_web_a['href'])
    
    if (i+1) % 2 == 0:
        print(f"Scraped {i+1} pages")


print(company_websites);

df = pd.DataFrame({'Name': company_names, 'Website': company_websites})

df.to_csv('Scovelo.csv')

print("CSV file created successfully")