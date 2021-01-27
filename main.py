import requests
import random
from bs4 import BeautifulSoup
import re
import pandas

def get_page(url):
    url_list = (
        {'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv2.0.1) Gecko/20100101 Firefox/4.0.1"},
        {'user-agent': "Mozilla/5.0 (Windows NT 6.1; rv2.0.1) Gecko/20100101 Firefox/4.0.1"},
        {'user-agent': "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11"},
        {'user-agent': "Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11"},
        {'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11"}
    )
    user_agent = random.choice(url_list)
    response = requests.get(url, headers=user_agent)
    if response.status_code == 200:
        return response.text


def get_onepage_data(html):
    soup = BeautifulSoup(html, 'html.parser')
    data_one_page,data = [],[]
    for item in soup.select('div.item'):
        item = str(item)
        sub_soup = BeautifulSoup(item,'html.parser')
        link = sub_soup.select('div.pic a')[0]['href']
        name = sub_soup.select('li.title a em')[0].text
        try:
            cname = re.search('.*\s/',name).group()[:-2]
            oname = re.search('/\s.*',name).group()[2:]
        except AttributeError:
            cname = name
            oname = name
        intro = sub_soup.select('li.intro')[0].text
        try:
            date = re.search('\d{4}-\d*-\d*', intro).group()
        except AttributeError:
            date = ''
        try:
            rating = sub_soup.findAll('span', class_=re.compile('rating.*'))[0]['class'][0][6:-2]
        except IndexError:
            rating = ''
        mark_date = sub_soup.findAll('span',class_ = re.compile('date'))[0].text
        try:
            tags = sub_soup.findAll('span',class_ = re.compile('tags'))[0].text[4:]
        except IndexError:
            tags = ''
        data = [link,cname,oname,date,rating,mark_date,tags]
        data_one_page.append(data)
    print(data_one_page)
    return data_one_page


def save_data(all_data):
    col =['link','cname','oname','date','rating','mark_date','tags']
    file = pandas.DataFrame(columns=col,data=all_data)
    file.to_csv('watchedMoviesOnDouban.csv')


def get_all_data(url):
    all_data,one_page_data = [],[]
    temp_url = url
    count = 0
    while True:
        count = count + 1
        try:
            soup = BeautifulSoup(get_page(temp_url),'html.parser')
            all_data.extend(get_onepage_data(get_page(temp_url)))
            sub_url = soup.select('span.next a')[0]['href']
            temp_url = "https://movie.douban.com"+sub_url
        except IndexError:
            return all_data



def main():
    url = "https://movie.douban.com/people/everwhat/collect"
    save_data(get_all_data(url))

if __name__ == "__main__":
    main()
