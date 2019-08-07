from flask import Flask

app = Flask(__name__)

from Server.app.api.user_rank import user_rank_api

app.add_url_rule('/user/rank', 'user_rank_api', user_rank_api)

if __name__ == '__main__':
    app.run(host='172.30.1.59', port= 5000, debug= True)