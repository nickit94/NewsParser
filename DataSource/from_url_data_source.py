import re
import requests
from requests.exceptions import HTTPError


# TODO: вынести в отдельный файл
def is_valid_url(url):
    return re.search(r'^https?:\/\/.+', url)


class FromUrlDataSource:
    """
    Получение данных для парсинга с URL.
    """

    def __init__(self, url):
        self.url = url

    def get_data(self):

        if not is_valid_url(self.url):
            print('Invalid URL')
            return None

        try:
            response = requests.get(self.url)
            response.raise_for_status()
        except HTTPError as http_err:
            print('HTTP error occurred: {}'.format(http_err))
            return None
        except Exception as err:
            print('Other error occurred: {}'.format(err))
            return None
        else:
            print('Page loaded successfully!')

        return response
