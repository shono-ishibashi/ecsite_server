from flask import Blueprint, request, jsonify

# from . import models

import models
import auth_util

api = Blueprint('api', __name__, url_prefix='/flask')


@api.route('/', methods=['GET'])
def request_test():
    return jsonify({'test': 'hello! this is flask container'})


@api.route('/order-history/', methods=['GET'])
def fetch_order_history():
    """
    ログイン中のユーザーの注文履歴を取得するメソッド
    """
    token = request.headers.get('Authorization')
    response = auth_util.fetch_login_user(token)

    # 401がauthサーバーから返って来たなら401を返す
    if response.status_code == 401:
        return jsonify({}), 401

    # limit offset を作成
    offset = request.args.get("offset", default=0, type=int)
    limit = request.args.get("limit", default=5, type=int)

    login_user_id = response.json()['user']['id']

    # カートの状態でない注文を取得
    orders = models.Order.query \
        .filter(models.Order.user_id == login_user_id) \
        .filter(models.Order.status != 0) \
        .order_by(models.Order.order_date.desc()) \
        .limit(limit) \
        .offset(offset) \
        .all()

    order_schema = models.OrderSchema(many=True)

    return jsonify({'orders': order_schema.dump(orders)}), 200


@api.route('/order-history/count/')
def fetch_order_history_count():
    """
    ログイン中の注文履歴の総数を取得するメソッド
    """
    token = request.headers.get('Authorization')
    response = auth_util.fetch_login_user(token)

    if response.status_code == 401:
        return jsonify({}), 401

    login_user_id = response.json()['user']['id']

    # カートの状態でない注文を取得
    order_history_count = models.Order.query \
        .filter(models.Order.user_id == login_user_id) \
        .filter(models.Order.status != 0) \
        .count()
    return jsonify({'count': order_history_count}), 200
