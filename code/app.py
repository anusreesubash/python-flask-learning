from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required

from security import authenticate, identity

app = Flask(__name__)
app.secret_key = 'anusree'
api = Api(app)

jwt = JWT(app, authenticate, identity)

items = [
{
  'name': 'chair',
  'price': 56
}
]

class Item(Resource):
  parser = reqparse.RequestParser()
  parser.add_argument('price',
    type = float,
    required = True,
    help = 'this cannot be left blank'
    )
  data = parser.parse_args()
  @jwt_required() 
  def get(self, name):
    item = next(filter(lambda x: x['name'] == name, items), None)
    return {'item': item}, 200 if item else 404

  def delete(self, name):
    global items
    items = list(filter(lambda x: x['name'] == name, items))
    return {'message': 'item deleted'}

  def put(self, name):
    item = next(filter(lambda x: x['name'] == name,items), None)
    if item == None:
      item = {'name': name, 'price': data['price']}
      items.append(item)
    else:
      item.update(data)
    return item

  def post(self, name):
    if next(filter(lambda x: x['name'] == name, items), None):
      return {'message': 'This item already exists'.format(name)}
    data = Item.parser.parse_args()
    item = {'name': name, 'price': data['price'] }
    items.append(item)
    return item, 201

class ItemList(Resource):
  def get(self):
    return{'items': items}
    

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')

app.run(port=5000, debug=True)