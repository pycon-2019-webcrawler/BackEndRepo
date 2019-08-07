import requests
import json
from Server.Data.api_key.api_key import api_key


def user_rank_func(user_name):
    total_dict = {}

    url = 'https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-name/' + user_name + api_key

    res = requests.get(url=url)
    summoner_id = json.loads(res.text)['id']

    url = 'https://kr.api.riotgames.com/lol/league/v4/entries/by-summoner/' + summoner_id + api_key

    res = requests.get(url=url)
    user_data = json.loads(res.text)

    if user_data == []:
        print('언랭이네요')
        return ''

    queue_list = []
    for i in user_data:
        queue_list.append(i['queueType'])

    if 'RANKED_SOLO_5x5' in queue_list:
        solo_dict = {}

        solo_data = user_data[queue_list.index('RANKED_SOLO_5x5')]
        solo_dict['tire'] = solo_data['tier']
        solo_dict['rank'] = solo_data['rank']
        solo_dict['lP'] = solo_data['leaguePoints']
        solo_dict['wins'] = solo_data['wins']
        solo_dict['losses'] = solo_data['losses']

        total_dict['RANKED_SOLO_5x5'] = solo_dict

    if 'RANKED_FLEX_SR' in queue_list:
        flex_dict = {}

        flex_data = user_data[queue_list.index('RANKED_SOLO_5x5')]
        flex_dict['tire'] = flex_data['tier']
        flex_dict['rank'] = flex_data['rank']
        flex_dict['lP'] = flex_data['leaguePoints']
        flex_dict['wins'] = flex_data['wins']
        flex_dict['losses'] = flex_data['losses']

        total_dict['RANKED_FLEX_SR'] = flex_dict

    return total_dict