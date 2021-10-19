import requests
import bs4
from pprint import pprint

response = requests.get('https://habr.com/ru/all/')
response.raise_for_status()
#print(response.text)

soup = bs4.BeautifulSoup(response.text, features='html.parser')

article = soup.find('article')
#print(article.text)

articles = soup.find_all('article')
KEYWORDS = {'дизайн', 'фото', 'web', 'python'}
cnt = 0
for article in articles:
#    words = article.text.split(' ')
    hubs = article.find_all(class_='tm-article-snippet__hubs-item')
    hubs = set(hub.find('span').text for hub in hubs)
    title = article.find(class_='tm-article-snippet__title-link')
    title = set(title.find('span').text.split(' '))
    #paragraphs = article.find(class_='article-formatted-body article-formatted-body_version-2').find('p').text
    #paragraphs = (article.find("div", class_="article-formatted-body article-formatted-body_version-2").find("p").text)
    # if paragraphs == None:
    #     paragraphs = (article.find("div", class_="article-formatted-body article-formatted-body_version-2").find("p").text)
    #     paragraphs = article.find(class_='article-formatted-body article-formatted-body_version-2')
    cnt +=1

    #paragraphs = paragraphs.find_all('p').text
    try:
        paragraphs = article.find(class_='article-formatted-body article-formatted-body_version-2').find('p').text
    except AttributeError as e:
         pass
    # else:
    #     paragraphs = article.find(class_='article-formatted-body article-formatted-body_version-1').find('p').text
    if KEYWORDS & title or KEYWORDS & hubs:
        href = article.find(class_='tm-article-snippet__title-link').attrs['href']
        link = 'https://habr.com' + href
        print(article.find('h2').text, '-', link)
    print(cnt)
    print(paragraphs)









