from flask import Blueprint, request, jsonify

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

    print("aaaaaaaaaaaaaaaaaaaaaaaaa")
    print(vars(response))
    print("aaaaaaaaaaaaaaaaaaaaaaaaa")
    login_user_id = response.json()['user']['id']

    # カートの状態でない注文を取得
    orders = models.Order.query \
        .filter(models.Order.user_id == login_user_id) \
        .filter(models.Order.status != 0) \
        .order_by(models.Order.order_date.desc(), models.Order.id.desc()) \
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


@api.route('/item/', methods=['GET'])
def fetch_item_list():
    """
    商品一覧を取得するメソッド
    デフォルトでの並び順は安価順
    商品名を指定しなれけば全件取得
    商品名での検索は部分一致で行っている
    検索の結果、該当するデータが無ければ空のlistを返す
    """
    item_name = request.args.get("item_name", default='', type=str)
    sort_id = request.args.get("sort_id", default=0, type=int)
    if sort_id == 1:
        # sort_idが1なら高価順に並び替え
        items = models.Item.query \
            .filter(models.Item.name.like(f'%{item_name}%')) \
            .order_by(models.Item.price_m.desc(), models.Item.name.asc()) \
            .all()
    else:
        # sort_idが1以外なら安価順に並び替え
        items = models.Item.query \
            .filter(models.Item.name.like(f'%{item_name}%')) \
            .order_by(models.Item.price_m.asc(), models.Item.name.asc()) \
            .all()

    item_schema = models.ItemSchema(many=True)
    return jsonify(
        {'items': item_schema.dump(items)}), 200


@api.route('/item-name/', methods=['GET'])
def fetch_item_name():
    """
    オートコンプリート用の全商品の名前を取得するメソッド
    """
    item_name_list = models.Item.query.with_entities(models.Item.name).all()
    item_names = []
    for item_name in item_name_list:
        item_names.append(item_name[0])
    return jsonify({"item_names": item_names}), 200


@api.route('/item/<int:item_id>/', methods=['GET'])
def fetch_item_detail(item_id):
    """
    商品詳細を取得するメソッド
    """
    item = models.Item.query.get(item_id)
    if item:
        item_schema = models.ItemSchema()
        return jsonify({"item": item_schema.dump(item)}), 200
    else:
        return jsonify({}), 404


@api.route('/topping/', methods=['GET'])
def fetch_topping_list():
    """
    トッピング一覧を取得するメソッド
    """
    toppings = models.Topping.query.all()
    topping_schema = models.ToppingSchema(many=True)
    return jsonify({"topping": topping_schema.dump(toppings)}), 200
