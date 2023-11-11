from seleniumwire import webdriver as seleniumwire
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import sys
import pandas as pd
from time import sleep

class Scraper:
    
    def __init__(self):
        options = Options()
        options.add_argument("--incoignito")
        self.driver = seleniumwire.Chrome(options=options)
        self.actions = ActionChains(self.driver)
        self.url = 'https://www.facebook.com/'
        self.login()
        self.scrape_data()

    def login(self):
        try:
            driver = self.driver
            actions = self.actions
            driver.get(self.url)
            sleep(3)
            user_element = driver.find_element(By.ID, 'email')
            username = input('Enter your username. - ')
            password = input('Enter your password. - ')
            user_element.send_keys(username)
            sleep(2)
            actions.send_keys(Keys.TAB).perform()
            sleep(2)
            actions.send_keys(password).perform()
            sleep(2)
            actions.send_keys(Keys.ENTER).perform()
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//a[@aria-label="Facebook"]')))
            print('You are logged in Successfully.')
        except Exception as error:
            print(error)
            driver.close()
            sys.exit()
            
    def scroll_down(self):
        try:
            body = self.driver.find_element(By.XPATH, '/html/body')
            body.click()
            sleep(1)
            for _ in range(10):
                body.send_keys(Keys.SPACE)
                sleep(2)
        except:
            print('Something is wrong.')
            self.driver.close()
            sys.exit()

    def scrape_data(self):
        driver = self.driver
        driver.get('https://www.facebook.com/esenseit')
        data = {
            'Profile':[],
            'Url':[],
            'Text':[]
        }
        url = None
        self.scroll_down()
        try:
            profile = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div/div/div[1]/div[2]/div/div/div/div[3]/div/div/div[1]/div/div/span/h1').text
            all_elements = self.driver.find_element(By.XPATH, '//div[@data-pagelet="ProfileTimeline"]')
            descriptions = self.driver.find_elements(By.XPATH, '//*[@data-ad-comet-preview="message"]')
            links = all_elements.find_elements(By.XPATH, '//a[@role="link"]')
            done = 0
            for desc in descriptions:
                if done<5:
                    if desc.text != '':
                        data['Text'].append(desc.text)
                        done+=1
            for link in links:
                if link.text == profile:
                    url = link.get_attribute('href')
                    break
            for _ in range(5):
                data['Profile'].append(profile)
                data['Url'].append(url)
            df = pd.DataFrame(data)
            df.to_excel('fb_results.xlsx', index=False)
            print('Success')
        except Exception as error:
            print(error)

if __name__ == '__main__':
    scraper = Scraper()
