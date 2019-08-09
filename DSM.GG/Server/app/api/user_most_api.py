from Server.app.Function.user_most_func import user_most_func
from flask import request


def user_most_apI():
    user_name = request.json['summoner']
    return user_most_func(user_name)