# from flask_sqlalchemy import SQLAlchemy
#
# db = SQLAlchemy()
#
#
# class User(db.Model):
#     # テーブル名
#     __tablename__ = 'user'
#
#     # カラム情報
#     id = db.Column(db.Integer())
#     name = db.Column(db.Text())
#     test = db.Column(db.Integer, nullable=False)
#     create_time = db.Column(db.DateTime, nullable=False)
#     update_time = db.Column(db.DateTime, nullable=False)
#
#     def __init__(self, name, age):
#         self.name = name
#         self.age = age
#
#     def to_dict(self):
#         return {
#             'id': self.id,
#             'name': self.name,
#             'age': self.age,
#             'create_time': self.create_time,
#             'update_time': self.update_time
#         }
#
#
# class Item(db.Model):
#     __tablename_ = 'items'
#
#     id = db.Column(db.Integer, primary_key=True)
#     id = db.Column(db.Integer, primary_key=True)
#     id = db.Column(db.Integer, primary_key=True)
#     id = db.Column(db.Integer, primary_key=True)
#     id = db.Column(db.Integer, primary_key=True)
