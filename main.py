from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

app = Flask(__name__)

# Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# Cafe TABLE Configuration
class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)

    def __repr__(self):
        return f"Cafe {self.name} in {self.location}"

    def to_dict(self):
        """Creat dictionary using given Model"""
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}


@app.route("/")
def home():
    return render_template("index.html")


# HTTP GET - Read Record
@app.route("/random")
def get_random_cafe():
    random_cafe = Cafe.query.order_by(func.random()).first()  # get random cafe from DB
    return jsonify(cafe=random_cafe.to_dict())


@app.route("/all")
def get_all_cafes():
    all_cafes = []
    for cafe in Cafe.query.all():
        all_cafes.append(cafe.to_dict())
    return jsonify(cafes=all_cafes)


@app.route("/search")
def search_for_cafe():
    query_location = request.args.get("loc")
    cafes_in_location = Cafe.query.filter_by(location=query_location).all()
    cafes = []
    if cafes_in_location:
        for cafe in cafes_in_location:
            cafes.append(cafe.to_dict())
        return jsonify(cafes=cafes)
    else:
        return jsonify(error={"Not Found": "There is no cafe in given location."})


if __name__ == '__main__':
    app.run(debug=True)
