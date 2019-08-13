from Server.app.Function.user_rank_func_new import user_rank_func_new
from flask import request

def user_rank_api():
    user_id = request.json['summoner']
    return user_rank_func_new(user_id)