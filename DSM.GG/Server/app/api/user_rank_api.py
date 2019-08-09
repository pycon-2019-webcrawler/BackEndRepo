from Server.app.Function.user_rank_func import user_rank_func
from flask import request

def user_rank_api():
    user_id = request.json['summoner']
    return user_rank_func(user_id)