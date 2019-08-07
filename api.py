import requests
from flask import request, jsonify
from datetime import datetime, timedelta
import time

from lists import champion_list, champion_img_list, queue_list

api_key = 'variable'

def search():
    start = time.time()
    try:
        summoner = request.json['summoner']
    except KeyError:
        return jsonify({'err': 'summoner_name_required'})

    if summoner == '':
        return jsonify({'err': 'summoner_name_required'})

    try:
        page = request.json['page']
    except KeyError:
        page = 0

    if type(page) != int:
        return jsonify({'err': 'page_must_be_integer'})

    if page != 0:
        page = page*10 + 1

    response = []

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

    enc_account_id = response_search_summoner['accountId']

    url_fetch_matchlist = f'https://kr.api.riotgames.com/lol/match/v4/matchlists/by-account/' \
                          f'{enc_account_id}?beginTime={int(datetime.timestamp(datetime.now() - timedelta(days=150)))*1000}' \
                          f'&endIndex={page+10}&beginIndex={page}&api_key={api_key}'

    try:
        response_fetch_matchlist = requests.get(url_fetch_matchlist).json()['matches']
    except KeyError:
        return jsonify({'err': 'not_found'}), 404

    # response.append
    # ({'profileIconId':
    # f'http://opgg-static.akamaized.net/images/profile_icons/profileIcon{response_search_summoner["profileIconId"]}.jpg'})
    # 소환사 아이콘

    for i in response_fetch_matchlist:
        user = {}
        user['myChampion'] = {'champion': champion_list[i['champion']],
                                  'championImg': champion_img_list[i['champion']]}
        user['time'] = datetime.fromtimestamp(i['timestamp']/1000)
        user['queue'] = queue_list[i['queue']]

        game_id = i['gameId']
        url_fetch_matchone = f'https://kr.api.riotgames.com/lol/match/v4/matches/{game_id}?api_key={api_key}'
        response_fetch_matchone = requests.get(url_fetch_matchone).json()

        game_duration = response_fetch_matchone['gameDuration']

        users_list = []
        users_champion_img_list = []

        for j in response_fetch_matchone['participantIdentities']:
            users_list.append(j['player']['summonerName'])
            if j['player']['accountId'] == enc_account_id:
                my_participant_id = j['participantId']

        for j in response_fetch_matchone['participants']:
            users_champion_img_list.append(champion_img_list[j['championId']])
            if j['participantId'] == my_participant_id:
                my_team_id = j['teamId']

                spell_1_id = j['spell1Id']
                spell_2_id = j['spell2Id']

                perk_main = j['stats']['perk0']
                perk_sub = j['stats']['perkSubStyle']

                item = [j['stats']['item0'], j['stats']['item1'], j['stats']['item2'], j['stats']['item3'],
                        j['stats']['item4'], j['stats']['item5'], j['stats']['item6']]

                kill = j['stats']['kills']
                death = j['stats']['deaths']
                assist = j['stats']['assists']

                level = j['stats']['champLevel']

                minion = j['stats']['totalMinionsKilled']
                neutral_minion = j['stats']['neutralMinionsKilled']

        score = 0

        for j in response_fetch_matchone['participants']:
            if j['teamId'] == my_team_id:
                score += j['stats']['kills']

        blue_player = []
        red_player = []

        for j in range(10):
            if j <= 4:
                blue_player.append([users_list[j], users_champion_img_list[j]])
            else:
                red_player.append([users_list[j], users_champion_img_list[j]])

                items = []
                for k in item:
                    if k != 0:
                        items.append(f'http://opgg-static.akamaized.net/images/lol/item/{k}.png?image=w_22&v=1')

        user['blueTeam'] = blue_player
        user['redTeam'] = red_player
        user['spell'] = [f'http://z.fow.kr/spell/{spell_1_id}.png', f'http://z.fow.kr/spell/{spell_2_id}.png']
        user['rune'] = [f'http://opgg-static.akamaized.net/images/lol/perk/{perk_main}.png?image=w_22&v=1',
                                  f'http://opgg-static.akamaized.net/images/lol/perkStyle/{perk_sub}.png?image=w_22&v=2']
        user['items'] = items
        user['kills'] = kill
        user['deaths'] = death
        user['assists'] = assist
        user['level'] = level
        user['gameDuration'] = f'{int(game_duration/60)}분{game_duration%60}초'
        user['grade'] = round((kill+assist)/death, 3)
        user['totalMinionsKilled'] = minion+neutral_minion
        user['MinionsPerMinute'] = round(user['totalMinionsKilled']/(game_duration/60), 1)
        user['TotalKill'] = score
        user['killInvolvementRate'] = f'{round(((kill+assist)/score)*100)}%'

        response.append(user)
    print(time.time()-start)
    return jsonify(response)
