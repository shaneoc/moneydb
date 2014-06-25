from datetime import date

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from moneylib.remote.common import xvfb

class MBNAConnection:
    def __init__(self, username, password, sitekey):
        self.username = username
        self.password = password
        self.sitekey = sitekey

    def get_transactions(self, from_date, to_date):
        with xvfb():
            try:
                driver = webdriver.Firefox()
                driver.implicitly_wait(60) # seconds

                def save_page(filename):
                    with open(filename, 'w', encoding='utf-8') as f:
                        f.write(driver.page_source)

                driver.get(
                        'https://www.onlineaccess.ca/NASApp/NetAccess/LoginDisplay')

                save_page('step1.html')
                username_field = driver.find_element_by_name('username')
                username_field.send_keys(self.username)
                driver.save_screenshot('step1.png')
                username_field.submit()

                save_page('step2.html')
                password_field = driver.find_element_by_name('password')
                password_field.send_keys(self.password)
                driver.save_screenshot('step2.png')
                password_field.submit()

                save_page('step3.html')
                summary_link = driver.find_element_by_partial_link_text(
                        'Smart Cash World MasterCard ending in ')
                assert 'AccountSnapshotDisplay?' in summary_link.get_attribute(
                        'href')
                driver.save_screenshot('step3.png')
                summary_link.click()

                save_page('step4.html')
                driver.save_screenshot('step4.png')

            finally:
                driver.quit()
