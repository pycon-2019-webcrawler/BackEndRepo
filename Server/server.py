from flask import Flask

app = Flask(__name__)

from Server.app.api.user_rank_api import user_rank_api
from Server.app.api.user_inform_api import user_inform_api

app.add_url_rule('/user/rank', 'user_rank_api', user_rank_api)
app.add_url_rule('/user/inform', 'user_inform_api', user_inform_api)

if __name__ == '__main__':
    app.run(host='172.30.1.59', port= 5000, debug= True)