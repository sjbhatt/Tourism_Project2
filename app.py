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


@app.route("/candlestick_arrivals")
def candlestick_arrivals():
    """Render Home Page."""
    return render_template("candlestick_arrivals.html")

@app.route("/candlestick_departures")
def candlestick_departures():
    """Render Home Page."""
    return render_template("candlestick_departures.html")


@app.route("/tourism_arrival_data")
def tourism_arrival_data():
    
    arrival_results = db.session.query (Tourists.country_name).filter(Tourists.arrivals != "", Tourists.year == 2017 ).\
        order_by(Tourists.arrivals.desc()).\
        all()
    
    top_country_list = []
    low_arrival_count = []
    high_arrival_count = []
    arrival_count_2008 = []
    arrival_count_2017 = []
        
    for x in arrival_results:
        top_country_list.append(x.country_name)

    for x in top_country_list:
        query_data =  db.session.query (Tourists.year, Tourists.arrivals).filter(Tourists.country_name == x).filter(Tourists.arrivals != "", Tourists.year >= 2008, Tourists.year<=2017).all()
        no_of_arrivals = []
        no_of_arrivals = [int(result[1]) for result in query_data]
        low_arrival_count.append(min(no_of_arrivals))
        high_arrival_count.append(max(no_of_arrivals))
        arrival_count_2008.append(no_of_arrivals[0])
        arrival_count_2017.append(no_of_arrivals[len(no_of_arrivals)-1])       
    
    trace = {
        "type" : "candlestick",
        "x" : top_country_list,
        "high" : high_arrival_count,
        "low" : low_arrival_count,
        "open" : arrival_count_2008,
        "close" : arrival_count_2017
    }

    return jsonify(trace)

@app.route("/tourism_departure_data")
def tourism_departure_data():
    
    departure_results = db.session.query (Tourists.country_name).filter(Tourists.departures != "", Tourists.year == 2017 ).\
        order_by(Tourists.departures.desc()).all()
    
    top_country_list = []
    low_departure_count = []
    high_departure_count = []
    departure_count_2008 = []
    departure_count_2017 = []
        
    for x in departure_results:
        top_country_list.append(x.country_name)

    for x in top_country_list:
        query_data_2 =  db.session.query (Tourists.year, Tourists.departures).filter(Tourists.country_name == x).filter(Tourists.departures != "", Tourists.year >= 2008, Tourists.year<=2017).all()
        no_of_departures = []
        no_of_departures = [int(result[1]) for result in query_data_2]
        low_departure_count.append(min(no_of_departures))
        high_departure_count.append(max(no_of_departures))
        departure_count_2008.append(no_of_departures[0])
        departure_count_2017.append(no_of_departures[len(no_of_departures)-1])       
    
    trace = {
        "type" : "candlestick",
        "x" : top_country_list,
        "high" : high_departure_count,
        "low" : low_departure_count,
        "open" : departure_count_2008,
        "close" : departure_count_2017
    }

    return jsonify(trace)


@app.route("/arriv_dep_data")
def tourism_arriv_dep_data():
    
    # Query for the top 10 emoji data
    # arrival_results = db.session.query (Tourists).filter(Tourists.year >= 2008, Tourists.year<=2017).\
    #     order_by(Tourists.arrivals.desc()).\
    #     limit(10).all()
    arrival_results = db.session.query (Tourists.arrivals,Tourists.departures,Tourists.country_iso,Tourists.country_name).filter(Tourists.arrivals != "").\
        filter(Tourists.year == 2017).order_by(Tourists.arrivals.desc()).\
        limit(1000).all()
    data=[]

    for arrivals, departures, country_iso, country_name in arrival_results:
        arrival_dct = {}
        arrival_dct["arrivals"] = arrivals
        arrival_dct["departures"] = departures
        arrival_dct["country_iso"] = country_iso
        arrival_dct["country_name"] = country_name
        data.append(arrival_dct)

    return jsonify(data)

@app.route("/arrivals")
def arrivals():
    """Render Arrivals Page."""
    return render_template("arrivals.html")

@app.route("/departures")
def departures():
    """Render Arrivals Page."""
    return render_template("departures.html")

@app.route("/combined_data")
def combined_data():
    """Render Arrivals Page."""
    return render_template("combinedData.html")

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
