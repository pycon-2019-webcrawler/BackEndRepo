import requests
from urllib.request import urlopen
from Data.Riot.Riot_list import champion_list, champion_img_list
from Data.api_key.api_key import api_key
from bs4 import BeautifulSoup
import json


def user_most_func(user_name):
    total_dict = {}

    url = f'https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-name/{user_name}?api_key={api_key}'
    summoner_id = json.loads(requests.get(url=url).text)['id']

    url = f'https://kr.api.riotgames.com/lol/champion-mastery/v4/scores/by-summoner/{summoner_id}?api_key={api_key}'
    total_dict['total_champion_score'] = requests.get(url=url).text

    url = f'https://kr.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-summoner/{summoner_id}?api_key={api_key}'
    most_champion_list = json.loads(requests.get(url=url).text)

    most_champion_dict = {}
    for i in range(3):
        index_dict = {}
        index_data = most_champion_list[i]
        print(index_data)

        index_dict['name'] = champion_list[index_data['championId']]
        index_dict['img'] = champion_img_list[index_data['championId']]
        index_dict['point'] = index_data['championPoints']
        index_dict['level'] = index_data['championLevel']

        most_champion_dict[i+1] = index_dict

    total_dict['champion'] = most_champion_dict


    return total_dict