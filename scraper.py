from bs4 import BeautifulSoup
from selenium import webdriver
import chromedriver_autoinstaller
import pandas as pd
from selenium.webdriver.common.by import By
from dotenv import load_dotenv
import os 

chromedriver_autoinstaller.install()

options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
options.add_argument('--headless')
driver = webdriver.Chrome(options=options)

print("Getting company data!")

# Don't delete this in any case

# company_websites = []
# company_names = []
# total_pages = 322

# for i in range(0,total_pages-1):
#     driver.get(f"https://clutch.co/us/agencies/digital?page={i}")

#     page_source = driver.page_source

#     soup = BeautifulSoup(page_source, 'lxml')

#     company_info = soup.find_all('h3', class_ = 'company_info')


#     for company in company_info:
#         if company.find('a'):
#             company_names.append(company.find('a').text.strip())

#     company_web_a_list = soup.find_all('a', class_ = 'website-link__item')

#     for company_web_a in company_web_a_list:
#         if '?' in company_web_a['href']:
#             company_websites.append(company_web_a['href'].rpartition('?')[0])
#         else:
#             company_websites.append(company_web_a['href'])
    
#     if (i+1) % 2 == 0:
#         print(f"Scraped {i+1} pages")


# print(company_websites);

# df = pd.DataFrame({'Name': company_names, 'Website': company_websites})

# df.to_csv('Scovelo.csv')

# print("CSV file created successfully")

# print(df)

load_dotenv()                    


user_name = os.environ.get('USERNAME')
password = os.environ.get('PASSWORD')

df = pd.read_csv('Scovelo.csv')

founders = []

# print(founders)
print("Getting company founder data")

driver.get("https://linkedin.com/uas/login")
  
usernameElement = driver.find_element(By.ID, "username")
usernameElement.send_keys(user_name)  # Enter Your Email Address
  
pword = driver.find_element(By.ID, "password")
pword.send_keys(password)        # Enter Your Password
  
driver.find_element(By.CSS_SELECTOR, ".login__form_action_container button").click()

counter = 0
for company in df['Name']:
    query = company + " founder"
    print(f"{company}")
    driver.get(f"https://www.google.com/search?q={query.replace(' ','+')}")
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'lxml')
    headers = soup.find_all('div', class_='yuRUbf')

    for header in headers:
        if "https://www.linkedin.com" in header.a["href"]:
            print(f"Profile URL: {header.a['href']}")
            profile_url = header.a['href']
            driver.get(profile_url)  
            page_source = driver.page_source
            soup = BeautifulSoup(page_source, 'lxml')
            try:
                founder = soup.find('h1', class_='text-heading-xlarge inline t-24 v-align-middle break-words').text
                print(founder)
                
                df.loc[df["Name"] == company, 'Founder'] = founder 

            except:
                df.loc[df["Name"] == company, 'Founder'] = "Error" 
                print("Some error occurred in current entry!")
            print(" ")
            break;

    counter += 1
    if counter % 10 == 0:
        df.to_csv('Scovelo.csv')
        print("Data updated to the CSV successfully")


# Direct method to find the founders
# for company in df['Name']:
#     query = company + " founder"
#     driver.get(f"https://www.google.com/search?q={query.replace(' ','+')}")
#     page_source = driver.page_source

#     soup = BeautifulSoup(page_source, 'lxml')

#     headers = soup.find_all('div', class_='yuRUbf')

#     for header in headers:
#         if "https://www.linkedin.com" in header.a["href"]:
#             # print(header.prettify())
#             print(header.a['href'])

#             break;
        
