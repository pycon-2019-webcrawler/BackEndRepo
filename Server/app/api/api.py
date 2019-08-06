import requests
from Server.Data.Champion.lists import champion_list, champion_img_list
from flask import Flask, request, jsonify

app = Flask(__name__)

api_key = 'RGAPI-ca7a485c-0e61-4983-8843-8954d3909e6e'

@app.route('/search', methods=['GET'])
def search():
    summoner = request.json['summoner']

    url_search_summoner = f'https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summoner}?api_key={api_key}'
    response_search_summoner = requests.get(url_search_summoner).json()
    try:
        response_search_summoner['status']
        return jsonify('잘못된 소환사 명')
    except KeyError:
        pass

    enc_id = response_search_summoner['id']
    enc_account_id = response_search_summoner['accountId']

    url_fetch_matchlist = f'https://kr.api.riotgames.com/lol/match/v4/matchlists/by-account/{enc_account_id}?api_key=RGAPI-ca7a485c-0e61-4983-8843-8954d3909e6e'
    response_fetch_matchlist = requests.get(url_fetch_matchlist).json()['matches']

    response = []

    for i in response_fetch_matchlist:
        temp = []
        temp.append({'champion': champion_list[i['champion']]})
        temp.append({'img': champion_img_list[i['champion']]})
        response.append(temp)

    return jsonify(response)


@app.route('/match-list', methods=['GET'])
def match_list():
    pass

if '__main__' == __name__:
    app.run(debug=True, port=5000, host='172.30.1.59')