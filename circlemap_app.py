import pandas as pd

from flask import (
    Flask,
    render_template,
    jsonify)

from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# The database URI
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///db/tourism.sqlite"

db = SQLAlchemy(app)

# Create our database model
class Tourists(db.Model):
    __tablename__ = 'intl_tourism'

    id = db.Column(db.Integer, primary_key=True)
    country_iso = db.Column(db.String)
    country_name = db.Column(db.String)
    year = db.Column(db.Integer)
    expd_pct_imp = db.Column(db.Float)
    expd_total = db.Column(db.Float)
    expd_trans = db.Column(db.Float)
    expd_items = db.Column(db.Float)
    arrivals = db.Column(db.Float)
    departures = db.Column(db.Float)
    rcpt_pct_exp = db.Column(db.Float)
    rcpt_total = db.Column(db.Float)
    rcpt_trans = db.Column(db.Float)
    rcpt_items = db.Column(db.Float)
    longitude = db.Column(db.Float)
    latitude = db.Column(db.Float)

    def __repr__(self):
        return '<Tourists %r>' % (self.name)

# Create database tables
@app.before_first_request
def setup():
    # Recreate database each time for demo
    # db.drop_all()
    db.create_all()

@app.route("/")
def home():
    """Render Home Page."""
    return render_template("index.html")

@app.route("/tourism_mapdata.json")
def tourism_lnglat_filter():
    """Return JSON for mapable tourism data"""
    map_data = db.session.query(Tourists.country_name,\
        Tourists.expd_pct_imp, Tourists.expd_total,\
        Tourists.rcpt_pct_exp, Tourists.rcpt_total,\
        Tourists.longitude, Tourists.latitude).\
        filter(Tourists.year == 2017).\
        filter(Tourists.expd_pct_imp != "").\
        filter(Tourists.longitude != "").\
        order_by(Tourists.country_name).all()

    map_pts = []
    
    for country in map_data:
        map_dict = {}
        map_dict['country_name'] = country.country_name
        map_dict['expd_pct_imp'] = country.expd_pct_imp
        map_dict['expd_total'] = country.expd_total
        map_dict['rcpt_pct_exp'] = country.rcpt_pct_exp
        map_dict['rcpt_total'] = country.rcpt_total
        map_dict['longitude'] = country.longitude
        map_dict['latitude'] = country.latitude
        map_pts.append(map_dict)
    
    return jsonify(map_pts)

if __name__ == '__main__':
    app.run(debug=True)
