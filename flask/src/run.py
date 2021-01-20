from flask import Flask, jsonify
from models import db

from flask_cors import CORS

from api import api

# Flask本体
app = Flask(__name__)
# ファイルから設定を読み込む
app.config.from_pyfile('conf.cfg')
# 文字化けを解消
app.config['JSON_AS_ASCII'] = False

CORS(app)


@api.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response


# DB初期化
db.init_app(app)

# Blueprint登録
app.register_blueprint(api)


@app.errorhandler(404)
def page_not_found(error):
    return jsonify({'error': {
        'code': 'Not found',
        'message': 'Page not found.'
    }}), 404


if __name__ == '__main__':
    app.run(host='localhost', port=8000, debug=True)
