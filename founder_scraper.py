from time import sleep
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

print("Getting founder data!")

load_dotenv()                    

user_name = os.environ.get('USERNAME')
password = os.environ.get('PASSWORD')

df = pd.read_csv('Scovelo.csv')

founders = []

driver.get("https://linkedin.com/uas/login")
  
try:
    usernameElement = driver.find_element(By.ID, "username")
    usernameElement.send_keys(user_name)  # Enter Your Email Address
    
    pword = driver.find_element(By.ID, "password")
    pword.send_keys(password)        # Enter Your Password
    
    driver.find_element(By.CSS_SELECTOR, ".login__form_action_container button").click()
except:
    print("Failed to login via LinkedIn, please try some other credentials")
    exit()

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
            sleep(2)
            page_source = driver.page_source
            soup = BeautifulSoup(page_source, 'lxml')
            try:
                founder = soup.find('h1', class_='text-heading-xlarge inline t-24 v-align-middle break-words').text
                print(f"Founder : {founder}")
                
                entry = df["Name"] == company
                df.loc[entry,'Founder'] = founder 

                try:
                    location = soup.find('span', class_='text-body-small inline t-black--light break-words').text.strip()
                    print(f"Location : {location}")
                    detailedLocation = location.split(',')
                    df.loc[entry,'City'] = detailedLocation[0]
                    try:
                        df.loc[entry,'State'] = detailedLocation[1]
                        try:
                            df.loc[entry,'Country'] = detailedLocation[2]
                        except:
                            print("Country details not available")
                    except:
                        print("State and Country details not available")
                except Exception as e:
                    print(e)
                    print("Location details not available.")
            except Exception as e:
                print(e)
                df.loc[df["Name"] == company, 'Founder'] = "Couldn't find details!" 
            print(" ")
            break

    counter += 1
    if counter % 10 == 0:
        df.to_csv('Scovelo.csv')
        print(f"\nData of {counter} founders updated to the CSV successfully")

# This code is for cleaning up the csv
for column in df.columns:
    if "Unnamed" in column:
        df.drop(columns=column, inplace=True, axis=1)

df.to_csv('Scovelo.csv')
        
