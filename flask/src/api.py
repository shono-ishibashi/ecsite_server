from flask import Blueprint, request, jsonify

# from .models import db, User

api = Blueprint('api', __name__, url_prefix='/flask')


# エンドポイント http:/host/api/users, GETメソッドのみ受け付ける
# routeは複数指定も可能、methodsはリストなので複数指定可能
# @api.route('/order_history', methods=['GET'])
# def fetch_order_historys():
#     # クエリーパラメータ取得 request.args.get
#     # 第一引数:パラメータ名、default=で初期値、type=で変換する型を指定できる
#     q_limit = request.args.get('limit', default=-1, type=int)
#     q_offset = request.args.get('offset', default=0, type=int)
#
#     if q_limit == -1:
#         # DBから全件取得
#         users = User.query.all()
#     else:
#         # DBからoffset, limitを使用して取得
#         users = User.query.offset(q_offset).limit(q_limit)
#
#     # jsonレスポンス返却
#     # jsonifyにdict型オブジェクトを設定するとjsonデータのレスポンスが生成される
#     return jsonify({'users': [user.to_dict() for user in users]})


@api.route('/test', methods=['GET'])
def request_test():
    return jsonify({'test': 'hello! this is flask container'})
