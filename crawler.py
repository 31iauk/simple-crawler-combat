import json
import requests
from bs4 import BeautifulSoup
import re
from db_settings import *


def get_index(item):
    # select_one()与fina()等效，查找一个实例
    index = item.select_one('i').text
    return index


def get_src(item):
    # select()查找所有带img标签的实例
    img_src = item.select('img')[1]
    template = re.compile('src="(.*?)"')
    img_src = ''.join(template.findall(str(img_src)))
    return img_src


def get_name(item):
    name = item.select('.name')[0].text
    name = re.sub('\n', '', name)
    return name


def get_actor(item):
    actor = item.select('.star')[0].text.split('：')[1]
    return actor


def get_time(item):
    time = item.select('.releasetime')[0].text.split('：')[1]
    return time


def get_score(item):
    score = item.select('.integer')[0].text + item.select('.fraction')[0].text
    return score


def get_dict(item):
    index = int(get_index(item))
    src = get_src(item)
    name = get_name(item)
    actor = get_actor(item)
    time = get_time(item)
    score = get_score(item)
    movies_dict = {'index': index, 'src': src, 'name': name, 'actor': actor, 'time': time, 'score': score}
    return movies_dict


def write_file(content):
    # 将 Python 对象编码成 JSON 字符串
    content = json.dumps(content, ensure_ascii=False)
    with open('result.txt', 'a') as f:
        f.write(content + '\n')


def write_to_mysql(content):
    src = content['src']
    name = content['name']
    actor = content['actor'].split('n')[0]
    time = content['time']
    score = content['score']
    data = Movies(src=src, name=name, actor=actor,time=time,score=score)
    session.add(data)
    session.commit()


if __name__ == '__main__':
    url = 'https://maoyan.com/board'
    # Python 告诉网站服务器它是一个 Python 程序，所以需要把header加上
    header = {"user-agent": "Mozilla/5.0 (MSIE 10.0; Windows NT 6.1; Trident/5.0)"}
    res = requests.get(url, headers=header)
    soup = BeautifulSoup(res.text, "html.parser")
    print(soup)
    for item in soup.select('dd'):
        movies_dict = get_dict(item)
        write_file(movies_dict)
        write_to_mysql(movies_dict)
