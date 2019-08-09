from flask import Flask, request
from flask_httpauth import HTTPBasicAuth
from flask_cors import CORS, cross_origin

app = Flask(__name__)
# CORS(app)

from Server.app.api.user_rank_api import user_rank_api
from Server.app.api.user_inform_api import user_inform_api
from Server.app.api.user_history_api import user_history_api
from Server.app.api.user_most_api import user_most_apI

app.add_url_rule('/user/rank', 'user_rank_api', user_rank_api, methods=['POST'])
app.add_url_rule('/user/inform', 'user_inform_api', user_inform_api, methods=['POST'])
app.add_url_rule('/user/history', 'user_history_api', user_history_api, methods=['POST'])
app.add_url_rule('/user/most', 'user_most_api', user_most_apI, methods=['POST'])


if __name__ == '__main__':
    app.run(host='172.30.1.59', port= 5000, debug= True)