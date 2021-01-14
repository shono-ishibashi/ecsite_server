from flask import Blueprint, request, jsonify

# from . import models

import models

api = Blueprint('api', __name__, url_prefix='/flask')


@api.route('/test/item', methods=['GET'])
def test_items():
    token = request.headers.get('Authorization')
    # ログインユーザーを取得
    login_user = models.UserUtil.query.filter(
        models.UserUtil.token == token).first()
    print('#################')
    print(vars(login_user))
    print('#################')
    orders = models.Order.query.filter(
        models.Order.user_id == login_user.user_id).all()
    print('#################')
    for order in orders:
        print(vars(order))
    print('#################')
    order_schema = models.OrderSchema(many=True)
    items = models.Item.query.all()
    item_schema = models.ItemSchema(many=True)
    return jsonify(
        {'items': item_schema.dump(items),
         'orders': order_schema.dump(orders)}), 200


@api.route('/test', methods=['GET'])
def request_test():
    return jsonify({'test': 'hello! this is flask container'})
