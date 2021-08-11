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
        self.__scrapper.start_searching()
        data_extracted = self.__scrapper.get_list_of_profile(page=self.__page)
        return self.__sanitize_data(data_extracted)

    def __sanitize_data(self, profiles: dict):
        data = []
        for profile in profiles['results']['profiles']:
            new_profile = {}
            new_profile.update(
                {
                    'id': profile.get('recno'),
                    'account': profile.get('ciphertext'),
                    'full_name': profile.get('shortName'),
                    'picture_url': profile.get('portrait'),
                }
            )
            new_profile.update({'address': profile.get('location')})

            data.append(new_profile)
        return data
