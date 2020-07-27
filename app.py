from flask import Flask, jsonify, request, render_template

# Create an app __name__ is a variable that gives each file a unique name
app = Flask(__name__)

stores = [
  {
    'name': 'my-store',
    'items': [
      {
        'name': 'item1',
        'price': '43'

      }
    ]
  }
]

# request app will understand
@app.route('/')
def home():               #method
  return render_template('index.html')

# post/store/data:(name:)
@app.route('/store', methods=['POST'])
def create_store():
  request_data = request.get_json() # allows to get data from json
  new_store = {
    'name': request_data['name'],
    'items': []
  }
  stores.append(new_store)
  return jsonify(new_store)
  

# get/store/<string:name>
@app.route('/store/<string:name>')
def get_store(name):
  #iterate over stores
  # if the store name matches return that
  # else return error
  for store in stores:
    if store['name'] == name:
      return jsonify(store)
    
    return jsonify({'message':'store not found'})


# get/store
@app.route('/store')
def get_stores():
  return jsonify({'stores':stores}) # since stores is a list and jasonify reads only dictionaries


# post/store/<string:name>/item {name:, price:}
@app.route('/store/<string:name>/item', methods=['POST'])
def create_item_in_store(name):
  for store in stores:
    if store['name'] == name:
      request_data = request.get_json()
      new_item = {
      'name': request_data['name'],
      'price': request_data['price']
      }
      store['items'].append(new_item)
      return jsonify(new_item)

  return jsonify({'message': 'store not found'})


# get/store/<string:name>/item
@app.route('/store/<string:name>/item')
def get_items_in_store(name):
  for store in stores:
    if store['name'] == name:
      return jsonify({'items': store['items']})
    
    return jsonify({'message':'store not found'})

# delete/store/<string:name>
@app.route('/store/<string:name>', methods=['DELETE'])
def delete_store(name):
  global stores
  store = next((x for x in stores if x['name'] == name), None)
  if store == None:
    return jsonify({'message':"store not found"})
  stores = list(filter(lambda x: x['name'] != name, stores))
  return jsonify({'message':'store deleted'})


#tell app to run
app.run(port=5000)
