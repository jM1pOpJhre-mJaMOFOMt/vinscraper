from flask import Flask, render_template, request, flash
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from sqlalchemy_utils import aggregated
import datetime
from sqlalchemy import or_
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = 'secret string'

db = SQLAlchemy(app)
moment = Moment(app)

class Car(db.Model):
    __tablename__ = 'cars'
    
    vin = db.Column(db.String(17), unique=True, nullable=False, primary_key=True)
    serial = db.Column(db.Integer(), nullable=False)
    model = db.Column(db.String())
    engine = db.Column(db.String())
    port_of_entry = db.Column(db.String())
    ext_color = db.Column(db.String())
    int_color = db.Column(db.String())
    transport = db.Column(db.String())
    sold_to = db.Column(db.String(), db.ForeignKey('dealers.dealer_code'))
    shipped_to = db.Column(db.String())
    price = db.Column(db.Integer())
    scraped_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __init__(self, vin, serial, model, engine, port_of_entry, ext_color, int_color, transport, sold_to, shipped_to, price):
        self.vin = vin
        self.serial = serial
        self.model = model
        self.engine = engine
        self.port_of_entry = port_of_entry
        self.ext_color = ext_color
        self.int_color = int_color
        self.transport = transport
        self.sold_to = sold_to
        self.shipped_to = shipped_to
        self.price = price
        
class Dealer(db.Model):
    __tablename__ = "dealers"

    dealer_code = db.Column(db.String(), primary_key=True)
    address = db.Column(db.String())

    @aggregated('cars', db.Column(db.Integer))
    def car_count(self):
        return db.func.count('1')

    cars = db.relationship('Car', backref='dealer', lazy='dynamic')

    def __init__(self, dealer_code, address):
        self.dealer_code = dealer_code
        self.address = address

def get_car(vin):
    car = Car.query.filter_by(vin=vin).first()
    return car

def get_dealer(dealer_code):
    dealer = Dealer.query.filter_by(dealer_code=dealer_code).first()
    return dealer

def get_dealer_cars(dealer_code):
    cars = Car.query.filter(or_(Car.sold_to == dealer_code, Car.shipped_to == dealer_code))
    return cars

def create_car(car):
    existing_car = get_car(car.vin)
    if (existing_car == None):
        try:
            db.session.add(car)
            db.session.commit()
            #cache.delete_memoized(__get_cars_from_db__)
        except IntegrityError as e:
            print(f"Error creating car {e}")
            db.session().rollback()

    return car

def create_dealer(dealer):
    existing_dealer = get_dealer(dealer.dealer_code)
    if existing_dealer == None:
        try:
            db.session.add(dealer)
            db.session.commit()
            #cache.delete_memoized(__get_dealers_from_db__)
        except IntegrityError as e:
            print(f"Error creating dealer {e}")
            db.session.rollback()
    elif existing_dealer.address == "":
        try:
            existing_dealer.address = dealer.address
            db.session.commit()
            return existing_dealer
        except IntegrityError as e:
            print(f"Error creating dealer {e}")
            db.session.rollback()
    return dealer

@app.route('/', strict_slashes=False)
@app.route('/cars', strict_slashes=False)
def cars():
    cars = Car.query.order_by(Car.scraped_date.desc()).all()
    return render_template("cars.html", cars=cars)

@app.route('/dealer/<dealer_code>', strict_slashes=False)
def dealer_info(dealer_code):
    dealer = get_dealer(dealer_code)
    cars = get_dealer_cars(dealer_code)
    return render_template("dealer.html", dealer=dealer, cars=cars)

@app.route('/dealers', strict_slashes=False)
def dealers():
    dealers = Dealer.query.order_by(Dealer.dealer_code.asc()).all()
    return render_template("dealers.html", dealers=dealers)

if __name__ == '__main__':
    db.create_all()
    app.run()
    
