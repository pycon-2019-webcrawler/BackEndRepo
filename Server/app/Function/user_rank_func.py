import requests
import json
from Server.Data.api_key.api_key import api_key
from Server.Data.Tier.Tier_list import Tier_img


def user_rank_func(user_name):
    '''
    :param user_name:
    :return: status code
    404 - User Name not found
    200 - Return Complete
    '''
    total_dict = {}

    url = f'https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-name/{user_name}?api_key={api_key}'

    res = requests.get(url=url)

    try:
        summoner_id = json.loads(res.text)['id']
    except:
        error_dict = {}
        error_dict['message'] = 'User Name not found'
        error_dict['code'] = 404
        return error_dict, 404

    url = f'https://kr.api.riotgames.com/lol/league/v4/entries/by-summoner/{summoner_id}?api_key={api_key}'

    res = requests.get(url=url)
    user_data = json.loads(res.text)
    print(user_data)

    queue_list = ['RANKED_SOLO_5x5', 'RANKED_FLEX_SR']

    for i in range(2):
        try:
            if user_data[i]['queueType'] == 'RANKED_SOLO_5x5':
                solo_dict = {}


                solo_data = user_data[queue_list.index('RANKED_SOLO_5x5')]
                solo_dict['tire'] = solo_data['tier']
                solo_dict['rank'] = solo_data['rank']
                solo_dict['lP'] = solo_data['leaguePoints']
                solo_dict['wins'] = solo_data['wins']
                solo_dict['losses'] = solo_data['losses']
                solo_dict['rate'] = int(solo_dict['wins']*100)//(int(solo_dict['wins'])+int(solo_dict['losses']))
                solo_dict['rank_img'] = Tier_img[solo_dict['tire']][solo_dict['rank']]

                total_dict['RANKED_SOLO_5x5'] = solo_dict

            else:
                flex_dict = {}

                flex_data = user_data[queue_list.index('RANKED_FLEX_SR')]
                flex_dict['tire'] = flex_data['tier']
                flex_dict['rank'] = flex_data['rank']
                flex_dict['lP'] = flex_data['leaguePoints']
                flex_dict['wins'] = flex_data['wins']
                flex_dict['losses'] = flex_data['losses']
                flex_dict['rate'] = int(flex_dict['wins'] * 100) // (int(flex_dict['wins']) + int(flex_dict['losses']))
                flex_dict['rank_img'] = Tier_img[flex_dict['tire']][flex_dict['rank']]
                total_dict['RANKED_FLEX_SR'] = flex_dict

        except IndexError:
            user_queue_list = []
            for j in user_data:
                user_queue_list.append(j['queueType'])

            for k in queue_list:
                if k not in user_queue_list:
                    unranked_dict = {}
                    unranked_dict['tire'] = 'Unranked'
                    unranked_dict['rank_img'] = Tier_img[unranked_dict['tire']]

                    total_dict[k] = unranked_dict

    return total_dict, 200