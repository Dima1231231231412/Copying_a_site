import requests
from bs4 import  BeautifulSoup
from requests.api import head
import time
from random import randrange
import json


## Словарь с заголовками
headers = {
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.174 YaBrowser/22.1.2.834 Yowser/2.5 Safari/537.36'
           }

## Сбор ссылок со всех страниц
def get_articles_urls(url):
    s = requests.Session() ##Создаём сессию
    response = s.get(url=url, headers=headers) ## Отправляем запрос на главную страницу

    soup = BeautifulSoup(response.text, 'lxml') ## Создаём объект BeautifulSoup
    nagination_count = int(soup.find('span', class_='navigations').find_all('a')[-1].text) ## Находим 'span' класса 'navigations' а после все теги 'a' и последний с помощью индекса -1.

    ## Список для каждой из новостей
    articles_urls_list = []

    ## Проходимся по всем страницам циклом
    for page in range(1,nagination_count+1):
        response = s.get(url=f'https://hi-tech.news/page/{page}/',headers=headers) ## Отправляем на ссылку запрос
        soup = BeautifulSoup(response.text,'lxml') ## Создаём объект Soupa

        ##Забираем ссылку на статью
        articles_url = soup.find_all('a',class_='post-title-a')

        ##Пробегаемся по списку ссылок
        for au in articles_url:
            art_url = au.get('href') ## Достаём ссылку из отрибута 'href' с помощью метода get
            articles_urls_list.append(art_url)

        #time.sleep(randrange(2,5))
        print (f'Обработал {page}/{nagination_count}')

    ##Запись в файл ссылок
    with open('articles_urls.text','w') as file:
        for url in articles_urls_list:
            file.write(f'{url}\n')

    return 'Работа по сбору ссылок выполнена!'
    # with open('index.html','w',encoding='utf-8') as file:
    #     file.write(response.text)

##Сбор данных
def get_data(file_path):
    ## Читаем все ссылки из файла в список
    with open(file_path) as file:
        urls_list = [line.strip() for line in file.readlines()] ##Обрезаем концы

    urls_count = len(urls_list)
    s = requests.Session()
    resulrt_data = []

    #Пробегаемся по списку со ссылками
    for url in enumerate(urls_list[:5]):
        response = s.get(url=url[1], headers=headers) ## Отправляем запрос на ссылку
        soup = BeautifulSoup(response.text,'lxml') ##Создание объекта Soup
        article_title = soup.find('div', class_='post-content').find('h1', class_='title').text.strip()
        article_date = soup.find('div', class_='post').find('div', class_='tile-views').text.strip()
        article_img = f"https://hi-tech.news/{soup.find('div', class_='post-media-full').find('img').get('src')}"
        article_text = soup.find('div', class_='the-excerpt').text.strip().replace('\n','')

        resulrt_data.append(
            {
                'original_url': url[1],
                'article_title':article_title,
                'article_date': article_date,
                'article_img' : article_img,
                'article_text': article_text
            }
        )
        print(f'Обработано {url[0] + 1}/{urls_count}')
        #print(f'{article_title}\n{article_date}\n{article_img}\n{10*"#"}')
        time.sleep(3)
    with open('resulrt.json','w', encoding='utf-8') as file:
        json.dump(resulrt_data,file, indent=4, ensure_ascii=False)
    return 'Данные собраны!'

def main():
    #print(get_articles_urls(url='https://hi-tech.news/'))
    get_data('articles_urls.text')
if __name__ == '__main__':
     main()