from flask import request

from Server.app.Function.user_inform_func import user_inform_func

def user_inform_api():
    user_id = request.json['summoner']
    return user_inform_func(user_id)