from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait 
from time import sleep
from inputs import username
from inputs import pw

class FollowersBot:
    def __init__(self, username, pw):
        self.username = username
        self.pw = pw
        self.driver = webdriver.Chrome("C:/webdrivers/chromedriver")
        self.driver.get("https://instagram.com")
        sleep(2)
        self.driver.find_element_by_xpath("//a[contains(text(), 'Log in')]")\
            .click()
        sleep(2)
        self.driver.find_element_by_xpath("//input[@name=\"username\"]")\
            .send_keys(username)
        self.driver.find_element_by_xpath("//input[@name=\"password\"]")\
            .send_keys(pw)
        self.driver.find_element_by_xpath('//button[@type="submit"]')\
            .click()
        sleep(4)
        self.driver.find_element_by_xpath("//button[contains(text(), 'Not Now')]")\
            .click()
        sleep(2)

    def find_unfollowers(self):
        self.driver.find_element_by_xpath("//a[contains(@href,'/{}')]".format(self.username))\
            .click()

        sleep(2)

        self.driver.find_element_by_xpath("//a[contains(@href,'/following')]")\
            .click()

        following = self._get_accounts()

        self.driver.find_element_by_xpath("//a[contains(@href,'/followers')]")\
            .click()

        followers = self._get_accounts()

        not_following_back = [user for user in following if user not in followers]
        print(not_following_back)

    def _get_accounts(self):
        
        WebDriverWait(self.driver, 10).until(lambda d: d.find_element_by_css_selector('div[role="dialog"]'))

        self.driver.execute_script('''
            var fDialog = document.querySelector('div[role="dialog"] .isgrP');
            fDialog.scrollTop = fDialog.scrollHeight
        ''')

        sleep(2)

        box = self.driver.find_element_by_xpath("/html/body/div[4]/div/div[2]")

        last_height = self.driver.execute_script("return arguments[0].scrollHeight", box)

        while True:
            # Scroll down to bottom
            self.driver.execute_script("arguments[0].scrollTo(0, arguments[0].scrollHeight);", box)

            # Wait to load page
            sleep(1)

            # Calculate new scroll height and compare with last scroll height
            new_height = self.driver.execute_script("return arguments[0].scrollHeight", box)
            if new_height == last_height:
                # If heights are the same it will exit the function
                break
            last_height = new_height
    
        links = box.find_elements_by_tag_name('a')
        names = [name.text for name in links if name.text != '']

        self.driver.find_element_by_xpath("/html/body/div[4]/div/div[1]/div/div[2]/button")\
            .click()
            
        return names

bot = FollowersBot(username, pw)
bot.find_unfollowers()