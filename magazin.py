import flask
from flask.ext.sqlalchemy import SQLAlchemy

app = flask.Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/student/WebApp/db.sqlite'
db = SQLAlchemy(app)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    price = db.Column(db.Integer)

@app.route('/')
def home():
    return flask.render_template('home.html', product_list=Product.query.all())

@app.route('/save', methods=['POST'])
def save():
    product = Product(name=flask.request.form['name'], price=flask.request.form['price'])
    db.session.add(product)
    db.session.commit()
    flask.flash("Product added")
    return flask.redirect('/')

@app.route('/edit/<int:product_id>', methods=['POST', 'GET'])
def edit(product_id):
    product = Product.query.get(product_id)
    if not product:
        flask.abort(404)
    if flask.request.method == 'POST':
        product.name = flask.request.form['name']
        product.price = flask.request.form['price']
        db.session.commit()
        return flask.redirect("/edit/%d" % product.id)
    return flask.render_template('edit.html', product=product)

@app.route('/api/list', methods=['POST', 'GET'])
def api_list():
    product_id_list = []
    product_name_list = []
    product_price_list = []

    for product in Product.query.all():
        product_id_list.append(product.id)
        product_name_list.append(product.name)
        product_price_list.append(product.price)
    return flask.jsonify({
       'id_list' : product_id_list,
       'name_list' : product_name_list,
       'price_list' : product_price_list
        })
        
@app.route("/api/product/<int:product_id>")
def api_product(product_id):
    for product in Product.query.all():
        if product.id == product_id:
            return flask.jsonify({
                'id' : product.id, 'name' : product.name
            })

@app.route("/api/product/create", methods=['POST'])
def api_product_create():
    print flask.request.get_json()
    product = Product(name=flask.request.get_json()['name'])
    db.session.add(product)
    db.session.commit()
    return flask.jsonify({'status':'ok', 'id': product.id})
    
@app.route("/api/product/<int:product_id>/update", methods=['POST'])
def api_product_update(product_id):
    product = Product.query.get(product_id)
    product.name = flask.request.get_json()['name']
    db.session.commit()
    return flask.jsonify({'status' : 'ok'})
    
@app.route("/api/product/<int:product_id>/delete", methods=['POST', 'GET'])
def api_product_delete(product_id):
    product = Product.query.get(product_id)
    db.session.delete(product)
    db.session.commit()
    return flask.jsonify({'status' : 'ok'})


db.create_all()
app.run(debug=True)
