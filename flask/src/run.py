from flask import Flask, jsonify
from flask_cors import CORS

from models import db
from api import api

# Flask本体
app = Flask(__name__)
# ファイルから設定を読み込む
app.config.from_pyfile('conf.cfg')
# 文字化けを解消
app.config['JSON_AS_ASCII'] = False

# CORS
CORS(app)

# DB初期化
db.init_app(app)

# Blueprint登録
app.register_blueprint(api)


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers',
                         'x-requested-with,content-type,accept,origin,authorization,x-csrftoken,accept-encoding')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response


@app.errorhandler(404)
def page_not_found(error):
    return jsonify({'error': {
        'code': 'Not found',
        'message': 'Page not found.'
    }}), 404


if __name__ == '__main__':
    app.run(host='localhost', port=8000, debug=True)
