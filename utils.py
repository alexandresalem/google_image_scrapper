import logging
import os
import time
import urllib.request as ulib

from selenium import webdriver

logging.basicConfig(filename='app.log', filemode='w')


class ImageSearch:
    def __init__(self, search, quantity: int, folder, **kwargs):
        """
        Search and download Google Image Photos to a specific folder in your computer

        :type search: The search term you are looking for
        :type quantity: Number of images you want to download
        :type folder: Folder where you want to save the photos locally

        """
        self.search = search
        self.quantity = quantity
        self.folder = folder
        self.image_format = kwargs['image_format'] if 'image_format' in kwargs else ['jpg', 'svg', 'jpeg', 'png']

    def download(self):
        path = os.path.realpath('chromedriver')
        # WINDOW_SIZE = "1920,1080"
        # chrome_options = Options()
        # chrome_options.add_argument("--headless")
        # chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
        # chrome_options.add_argument('--no-sandbox')
        driver = webdriver.Chrome(executable_path=path)

        # Searching for term in Google Images
        url = f'https://www.google.com/search?tbm=isch&q={self.search}'
        driver.get(url)
        time.sleep(0.5)

        # Adding results links to a list
        download_list = []
        i = 0
        while len(download_list) < self.quantity:
            try:
                driver.find_element_by_xpath(
                    f'/html/body/div[2]/c-wiz/div[3]/div[1]/div/div/div/div/div[1]/div[1]/div[{i}]/a[1]/div[1]/img').click()
                time.sleep(0.5)
                photo = driver.find_element_by_xpath(
                    '/html/body/div[2]/c-wiz/div[3]/div[2]/div[3]/div/div/div[3]/div[2]/c-wiz/div/div[1]/div[1]/div/div[2]/a/img').get_property(
                    'src')
                if photo[-3:].lower() in self.image_format:
                    download_list.append(photo)
            except Exception as e:
                logging.debug(e)
            finally:
                i += 1

        # Downloading results
        for link in download_list:
            _, ext = os.path.splitext(link)
            path = os.path.join(self.folder, f'{self.search}_{download_list.index(link)}{ext}')

            try:
                ulib.urlretrieve(link, path)
                logging.warning(f'File {path} saved')
            except Exception as e:
                logging.debug(e)
                logging.warning(f"Couldn't save {link}")
