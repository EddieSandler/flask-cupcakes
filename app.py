from flask import Flask, request, jsonify, render_template

from models import db, connect_db, Cupcake


app = Flask(__name__)
app.app_context().push()
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)

@app.route('/')
def cupcake_form():
    cupcakes=Cupcake.query.all()
    return render_template('index.html',cupcakes=cupcakes)

@app.route('/api/cupcakes')
def list_cupcakes():
    """Returns JSON w/ all cupcakes"""
    all_cupcakes = [cupcake.serialize() for cupcake in Cupcake.query.all()]
    return jsonify(cupcakes=all_cupcakes)

@app.route('/api/cupcakes/<int:id>')
def get_cupcake(id):
    """view info on a cupcake"""
    cupcake=Cupcake.query.get_or_404(id)
    return jsonify(cupcake=cupcake.serialize())


@app.route('/api/cupcakes',methods=['POST'])
def make_cupcake():
    """ Create a cupcake"""
    new_cupcake = Cupcake(flavor=request.json["flavor"],size=request.json["size"],
    rating=request.json["rating"],image=request.json["image"])
    db.session.add(new_cupcake)
    db.session.commit()
    response_json = jsonify(cupcake=new_cupcake.serialize())
    return (response_json, 201)


@app.route('/api/cupcakes/<int:id>',methods=['PATCH'])
def update_cupcake(id):
    """update  info on a cupcake"""
    cupcake=Cupcake.query.get_or_404(id)
    cupcake.flavor = request.json.get('flavor',  cupcake.flavor)
    cupcake.size = request.json.get('size',  cupcake.size)
    cupcake.rating = request.json.get('rating',  cupcake.rating)
    cupcake.image = request.json.get('image',  cupcake.image)
    db.session.commit()
    return jsonify(cupcake=cupcake.serialize())



@app.route('/api/cupcakes/<int:id>',methods=['DELETE'])
def delete_cupcake(id):
    """delete a cupcake"""
    cupcake=Cupcake.query.get_or_404(id)
    db.session.delete(cupcake)
    db.session.commit()
    return jsonify(message="deleted")
