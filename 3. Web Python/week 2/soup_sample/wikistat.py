from bs4 import BeautifulSoup
import re
import os


# Вспомогательная функция, её наличие не обязательно и не будет проверяться
def build_tree(start, end, path):
    link_re = re.compile(r"(?<=/wiki/)[\w()]+")  # Искать ссылки можно как угодно, не обязательно через re
    files = dict.fromkeys(os.listdir(path))  # Словарь вида {"filename1": None, "filename2": None, ...}
    # TODO Проставить всем ключам в files правильного родителя в значение, начиная от start
    return files


# Вспомогательная функция, её наличие не обязательно и не будет проверяться
def build_bridge(start, end, path):
    files = build_tree(start, end, path)
    bridge = []
    # TODO Добавить нужные страницы в bridge
    return bridge



def parse(start, end, path):
    out={}
    
    for url in [start,end]:
    
        with open(path+url, 'r', encoding='utf-8') as f:
            html = f.read()
            soup=BeautifulSoup(html, 'lxml')    
            body = soup.find(id="bodyContent")
            img=body.find_all('img')
            count_img=len([x for x in img if x.get('width') and int(x.get('width')) >= 200])

            count_tags=0
            for x in range(1,7):
                title = body.find_all("h"+str(x))
                for y in title:
                    if y.text[0] in 'ETC':
                        count_tags+=1
                        #print(y.text)

            max_tags=0
            link_a=soup.find_all('a')
            for link in link_a:
                current_count = 1
                siblings = link.find_next_siblings()
                for sibling in siblings:
                    if sibling.name == 'a':
                        current_count += 1
                        max_tags = max(current_count, max_tags)
                    else:
                        current_count = 0
            #print(max_tags)

            count_list = 0
            lists = body.find_all(['ul', 'ol'])
            for tag in lists:
                if not tag.find_parents(['ul', 'ol']):
                    count_list += 1
            #print(count_list)
        out[url]=[count_img, count_tags, max_tags, count_list]
    return out