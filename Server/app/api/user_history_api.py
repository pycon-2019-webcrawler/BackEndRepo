from flask import request, jsonify
from Server.app.Function.user_history_func import user_history_func


def user_history_api():
    try:
        summoner = request.args['summoner']
    except KeyError:
        return jsonify({'err': 'summoner_name_required'})

    try:
        page = request.args['page']
    except KeyError:
        page = 0

    try:
        page = int(page)
    except ValueError:
        return jsonify({'err': 'page_must_be_integer'})

    return user_history_func(summoner, page)
