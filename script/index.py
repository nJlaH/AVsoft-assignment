from SpiderClass import Spider
import concurrent.futures
from datetime import datetime

host = 'localhost'
user = 'root'  # Пользователь базы данных
password = 'root'  # Пароль базы данных
database = 'spider'  # имя базы данных
site = 'http://google.com/'  # Сайт, который необходимо спарсить
ignore = ''  # Если встречаем эту подстроку в url, то пропускаем этот url
thread_limit = 30  # Лимит потоков

# Парсит ссылки из страницы, отмечает её обработанной и записывает новые ссылки в базу
def get_links_to_stream(link):
    spider = Spider(host, user, password, database)
    links = spider.get_links(link, ignore=ignore)
    spider.prepare_links(links, ignore)
    return f'Link {link} done'

start_time = datetime.now()
spider = Spider(host, user, password, database)
links = spider.get_links(site, ignore=ignore)
spider.prepare_links(links, ignore)

# while links != None and len(links) > 0:
while links != None and len(links) > 0:
    with concurrent.futures.ThreadPoolExecutor(thread_limit) as executor:
        futures = []
        links = spider.get_new_links(site)
        for link in links:
            link = link[0]
            futures.append(executor.submit(get_links_to_stream, link=link))  # запускаем поток и парсинг
    break

finish_time = datetime.now()
difference = finish_time - start_time
difference_in_s = difference.total_seconds()
days = divmod(difference_in_s, 86400)
hours = divmod(days[1], 3600)
minutes = divmod(hours[1], 60)
seconds = divmod(minutes[1], 1)
print("Время выполнения скрипта: %d дней, %d часов, %d минут and %d секунд" % (days[0], hours[0], minutes[0], seconds[0]))