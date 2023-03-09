import configparser
import requests
from bs4 import BeautifulSoup
from libretranslatepy import LibreTranslateAPI
import os

def get_settings():
    settings = configparser.ConfigParser()
    settings.read('config.cfg')
    url = settings.get('SETTINGS', 'url')
    source_lang = settings.get('SETTINGS', 'source_lang')
    target_lang = settings.get('SETTINGS', 'target_lang')
    headers = {'User-Agent': settings.get('User-Agent', 'value')}
    return url, source_lang, target_lang, headers

class Translator:
    def __init__(self):
        self.url, self.source_lang, self.target_lang, self.headers = get_settings()

    def fetch_data(self):
        print('Fetcihg data...')
        response = requests.get(self.url, headers=self.headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup

    def translate(self, text):
        translator = LibreTranslateAPI("https://translate.argosopentech.com/")
        translated_text = translator.translate(text, self.source_lang, self.target_lang)
        return translated_text

    def save_translation(self, soup):
        print('Saving translate...')
        with open('translated.html', 'w', encoding='utf-8') as f:
            f.write(str(soup))

    def run(self):

        soup = self.fetch_data()

        print('Translating...')
        text_elements = [element for element in soup.find_all(string=True) if element.parent.name not in ['script', 'style']]
        for element in text_elements:
            text = element.get_text(strip=True)
            if not text:
                continue
            translated_text = self.translate(text)
            element.replace_with(translated_text)

        self.save_translation(soup)

if __name__ == '__main__':

    if not os.path.isfile('config.cfg'):
        print("config.cfg dosyası mevcut değil!")
    else:
        translator = Translator()
        translator.run()
