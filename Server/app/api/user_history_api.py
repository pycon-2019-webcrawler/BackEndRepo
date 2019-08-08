from flask import request, jsonify
from Server.app.Function.user_history_func import user_history_func


def user_history_api():
    try:
        summoner = request.json['summoner']
    except KeyError:
        return jsonify({'err': 'summoner_name_required'})

    try:
        page = request.json['page']
    except KeyError:
        page = 0

    return user_history_func(summoner, page)