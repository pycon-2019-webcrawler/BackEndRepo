import requests
from flask import jsonify

from ...Data.api_key.api_key import api_key


def user_rank_func_new(summoner):
    if summoner == '':
        return jsonify({'err': 'summoner_name_required'})

    url_search_summoner = f'https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summoner}?api_key={api_key}'
    response_search_summoner = requests.get(url_search_summoner).json()

    try:
        err = response_search_summoner['status']['status_code']
        if err == 403:
            return jsonify({'err': 'token_expired'}), 403

        if err == 500:
            return jsonify({'err': 'invalid_summoner'}), 500

    except KeyError:
        pass

    response = {}
    solo_rank = {}
    flex_rank = {}

    enc_id = response_search_summoner['id']

    url_search_rank = f'https://kr.api.riotgames.com/lol/league/v4/entries/by-summoner/{enc_id}?api_key={api_key}'
    response_search_rank = requests.get(url_search_rank).json()

    for i in response_search_rank:
        if i['queueType'] == 'RANKED_SOLO_5x5':
            solo_rank['tier'] = i['tier']
            solo_rank['rank'] = i['rank']
            solo_rank['lp'] = i['leaguePoints']
            solo_rank['wins'] = i['wins']
            solo_rank['losses'] = i['losses']
            solo_rank['rate'] = round(solo_rank['wins']/(solo_rank['wins'] + solo_rank['losses']) * 100, 2)
            if solo_rank['rank'] == 'I':
                rank_to_int = 1
            elif solo_rank['rank'] == 'II':
                rank_to_int = 2
            elif solo_rank['rank'] == 'III':
                rank_to_int = 3
            elif solo_rank['rank'] == 'IV':
                rank_to_int = 4
            solo_rank['rank_img'] = f'https://opgg-static.akamaized.net/images/medals/' \
                                    f'{solo_rank["tier"].lower()}_{rank_to_int}.png'
            response['RANKED_SOLO_5x5'] = solo_rank

        if i['queueType'] == 'RANKED_FLEX_SR':
            flex_rank['tier'] = i['tier']
            flex_rank['rank'] = i['rank']
            flex_rank['lp'] = i['leaguePoints']
            flex_rank['wins'] = i['wins']
            flex_rank['losses'] = i['losses']
            flex_rank['rate'] = round(flex_rank['wins'] / (flex_rank['wins'] + flex_rank['losses']) * 100, 2)
            if flex_rank['rank'] == 'I':
                rank_to_int = 1
            elif flex_rank['rank'] == 'II':
                rank_to_int = 2
            elif flex_rank['rank'] == 'III':
                rank_to_int = 3
            elif flex_rank['rank'] == 'IV':
                rank_to_int = 4
            flex_rank['rank_img'] = f'https://opgg-static.akamaized.net/images/medals/' \
                                    f'{flex_rank["tier"].lower()}_{rank_to_int}.png'
            response['RANKED_FLEX_SR'] = flex_rank

    try:
        response['RANKED_SOLO_5x5']
    except KeyError:
        solo_rank['tier'] = 'Unranked'
        solo_rank['rank_img'] = f'https://opgg-static.akamaized.net/images/medals/default.png'
        response['RANKED_SOLO_5x5'] = solo_rank

    try:
        response['RANKED_FLEX_SR']
    except KeyError:
        flex_rank['tier'] = 'Unranked'
        flex_rank['rank_img'] = f'https://opgg-static.akamaized.net/images/medals/default.png'
        response['RANKED_FLEX_SR'] = flex_rank

    return jsonify(response)
