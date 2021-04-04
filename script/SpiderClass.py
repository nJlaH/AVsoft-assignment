import mysql.connector
import requests
import re
from bs4 import BeautifulSoup
import time as timesleep

class Spider:
    directory = 'data/'

    # Подключение к базе данных
    def __init__(self, host='localhost', user='postgres', password='root', database='spider'):
        self.connection = mysql.connector.connect(host=host, user=user, password=password, database=database)
        self.cursor = self.connection.cursor()

    # функция удаления
    def __del__(self):
        self.cursor.close()
        self.connection.close()

    # Загрузка страницы
    def get_url(self, url):
        page = requests.get(url)
        return page.text

    # Вытаскиваем из html кода ссылки в тегах <a>
    def get_links(self, link, ignore):
        links = list()
        domain = self.get_domain(link)
        header = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:32.0) Gecko/20100101 Firefox/32.0', }
        html = requests.get(link, headers=header).text
        timesleep.sleep(1)  # пауза 1 секунда
        soup = BeautifulSoup(html, 'html.parser')
        a = soup.find_all("a", href=True)
        self.write_new_link(link, ignore)
        for link in a:
            if len(link) > 0:
                str_link = str(link['href'])
                if not str_link.startswith('http'):  # Проверяем, относительная ссылка или нет
                    if str_link not in ['#', '/']:
                        if str_link.startswith('/'):
                            str_link = str_link[1::]
                        links.append(domain + str_link)
                else:
                    if link is not None and str_link.startswith(domain):
                        links.append(str_link)
        return links

    # Возвращаем домен из ссылки
    def get_domain(self, link):
        site = re.match('http[s]*://.+?/', link)
        site = site.group(0)
        return site

    # Записываем ссылки в базу данных
    def write_new_link(self, link, ignore):
        if not self.link_exists(link):
            site = self.get_domain(link)
            if len(ignore) == 0 or ignore not in link:
                try:
                    self.cursor.execute("INSERT INTO `links` SET `site` = %s, `url` = %s", (site, link))
                    self.connection.commit()
                except:  # Сработает при дублировании ссылки
                    pass

    # Проверяем, есть ли ссылка в БД
    def link_exists(self, link):
        self.cursor.execute("SELECT * FROM `links` WHERE `url` = %s", (link,))
        link = self.cursor.fetchone()
        if link == None:
            return False
        else:
            return True

    # Обрабатываем все полученные ссылки
    def prepare_links(self, links, ignore):
        for link in links:
            if not self.link_exists(link):
                self.write_new_link(link, ignore)
        self.connection.commit()

    # Получаем необработанные ссылки
    def get_new_links(self, site, limit=5000):
        self.cursor.execute("SELECT `url` FROM `links` WHERE `site` = %s LIMIT %s", (site, limit))
        return self.cursor.fetchall()
