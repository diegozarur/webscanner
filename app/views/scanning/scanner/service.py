import json
from flask import current_app

from app.views.scanning.scanner.browser import get_remote_webdriver
from app.views.scanning.scanner.crawler import ScannerCrawler
from app.views.scanning.scanner.scraper import ScannerScraper


class Scanner:
    def __init__(self, page=1):
        self.__page: int = page
        self.__scrapper = ScannerScraper()
        self.__crawler = ScannerCrawler()

    def doing(self):
        self.__scrapper.driver = get_remote_webdriver()
        data_extracted = self.__scrapper.start_searching(page=self.__page)

        self.__save_raw_data(data_extracted)
        return self.__sanitize_data(data_extracted)

    def __sanitize_data(self, profiles: list):
        data = []
        for profile in profiles:
            new_profile = {}
            new_profile.update(
                {
                    'id': profile.get('recno'),
                    'account': profile.get('ciphertext'),
                    'picture_url': profile.get('portrait'),
                }
            )
            new_profile.update(profile['person']['personName'])
            new_profile.update({'address': profile.get('location')})

            data.append(new_profile)
        return data

    def __save_raw_data(self, profiles: list) -> None:
        folder = current_app.config['UPLOAD_FOLDER']

        json_file = open(f"{folder}/searching_profiles_page{self.__page}.json", "w")
        json.dump(profiles, json_file)
