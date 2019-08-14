from Data.api_key.api_key import api_key
import requests
import json
from bs4 import BeautifulSoup
import time

def user_inform_func(user_id):
    start = time.time()
    total_dict = {}

    url = 'https://www.op.gg/summoner/userName=' + user_id
    res = requests.get(url=url)
    html = res.text
    bs = BeautifulSoup(html, 'lxml')

    total_dict['profile_img'] = 'https:'+bs.find('img', class_='ProfileImage').get('src')

    try:
        old_str = bs.find('div', class_='borderImage').get('style')[22:]
        total_dict['profile_img_border'] = 'https:' + str(old_str.replace(";", "").replace(")",""))
    except AttributeError:
        total_dict['profile_img_border'] = ''

    total_dict['name'] = user_id
    total_dict['level'] = bs.find('div', class_='ProfileIcon').find('span').text

    try:
        total_dict['rank_constant'] = bs.find('span', class_='ranking').text
    except AttributeError:
        total_dict['rank_constant'] = ''

    rank_str = ''
    count = 0
    try:
        for i in list(bs.find('div', class_='LadderRank').find('a').text):
            if count == 3:
                rank_str = rank_str + i
            if i == ' ':
                count += 1
        total_dict['rank_percentage'] = rank_str.replace('(', '').replace('%', '').replace(' ', '')
    except AttributeError:
        total_dict['rank_percentage'] = ''




    print(time.time()-start)

    return total_dict