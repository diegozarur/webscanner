import json
import time

from selenium.webdriver.android.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from twocaptcha import TwoCaptcha

from config import Config


class ScannerScraper:
    def __init__(self):
        self.__driver: WebDriver
        self.__url = 'https://www.upwork.com/ab/ats-aas/api/profile-search/profiles'
        self.__solver = TwoCaptcha(Config.TWOCAPTCHA_KEY)

    def start_searching(self, page: int) -> list:
        try:
            self.__login()
            profiles_extracted = self.__get_list_of_profile(page)
            profile_with_more_details = self.__get_profile_detail(profiles_extracted['results']['profiles'])
            return profile_with_more_details
        except Exception as e:
            self.__driver.quit()
            raise e

    def __login(self):
        wait = WebDriverWait(self.__driver, 10)
        self.__driver.get(self.__url)

        wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="login_username"]')))
        time.sleep(.5)

        login_username_input = self.__driver.find_element_by_id('login_username')
        login_username_input.clear()
        login_username_input.send_keys(Config.UPWORK_USER)

        continue_button = self.__driver.find_element_by_id('login_password_continue')
        continue_button.click()
        time.sleep(.5)

        try:
            wait.until(EC.element_to_be_clickable((By.ID, "login_password")))
        except Exception as e:
            self.__solve_recaptcha()

        time.sleep(2)
        WebDriverWait(self.__driver, 20).until(EC.presence_of_element_located((By.ID, "login_password")))
        password_field = self.__driver.find_element_by_id('login_password')
        password_field.click()
        password_field.send_keys(Config.UPWORK_PASS)

        self.__driver.find_element_by_id('login_control_continue').click()

    def __get_list_of_profile(self, page: int) -> dict:
        if page:
            self.__url = f'{self.__url}?page={page}'
        time.sleep(1)

        button_raw_data = '//*[@id="rawdata-tab"]'
        button = WebDriverWait(self.__driver, 20).until(EC.presence_of_element_located((By.XPATH, button_raw_data)))
        button.click()

        pre_element = '/html/body/div/div/div/div[2]/div/div/div[2]/pre'
        tag_pre = WebDriverWait(self.__driver, 20).until(EC.presence_of_element_located((By.XPATH, pre_element)))
        data_in_string = tag_pre.get_attribute('innerHTML')

        return json.loads(data_in_string)

    def __get_profile_detail(self, profiles: list) -> list:
        for profile in profiles:
            url = f"https://www.upwork.com/freelancers/api/v1/freelancer/profile/{profile.get('ciphertext')}/details?"
            self.__driver.get(url)

            button_raw_data = '//*[@id="rawdata-tab"]'
            button = WebDriverWait(self.__driver, 20).until(EC.presence_of_element_located((By.XPATH, button_raw_data)))
            button.click()

            pre_element = '/html/body/div/div/div/div[2]/div/div/div[2]/pre'
            tag_pre = WebDriverWait(self.__driver, 20).until(EC.presence_of_element_located((By.XPATH, pre_element)))
            data_in_string = tag_pre.get_attribute('innerHTML')
            data = json.loads(data_in_string)
            profile.update({'person': data.get('person')})
        self.__driver.quit()
        return profiles

    def __solve_recaptcha(self):
        frames = self.__driver.find_elements_by_tag_name('iframe')
        for frame in frames:
            self.__driver.switch_to_frame(frame)
            time.sleep(.5)
            try:
                div_recaptcha = self.__driver.find_element_by_class_name("g-recaptcha")
                site_key = div_recaptcha.get_attribute('data-sitekey')

                result = self.__solver.recaptcha(
                    sitekey=site_key,
                    url=self.__driver.current_url,
                )
                solution = result.get('code').replace('\\n', '')
                self.__driver.execute_script(
                    "document.getElementById('g-recaptcha-response').innerHTML='{}';".format(solution)
                )
                self.__driver.execute_script("handleCaptcha('{}')".format(solution))
                time.sleep(1)
                self.__driver.switch_to_default_content()
            except Exception:
                self.__driver.switch_to_default_content()
                continue

    @property
    def driver(self):
        return self.__driver

    @driver.setter
    def driver(self, value):
        self.__driver = value
