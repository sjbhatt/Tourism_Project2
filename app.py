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


@app.route("/tourism_data")
def tourism_arrival_departure_data():
    
    # Query for the top 10 emoji data
    # arrival_results = db.session.query (Tourists).filter(Tourists.year >= 2008, Tourists.year<=2017).\
    #     order_by(Tourists.arrivals.desc()).\
    #     limit(10).all()
    arrival_results = db.session.query (Tourists.arrivals,Tourists.country_name).filter(Tourists.arrivals != "").\
        order_by(Tourists.arrivals.desc()).\
        limit(1000).all()
    data=[]
    for x in arrival_results:
        # print(data.arrivals)
        data.append(x.arrivals)
    return jsonify({'data':data})
"""    
    # departure_results = db.session.query (Tourists).filter(Tourists.year >= 2008, Tourists.year<=2017)#.\
        # order_by(Tourists.departures.desc()).\
        # limit(10).all()


    # Create lists from the query results
    emoji_char = [result[0] for result in results]
    scores = [int(result[1]) for result in results]

    # Generate the plot trace
    trace = {
        "x": emoji_char,
        "y": scores,
        "type": "bar"
    }
    return jsonify(trace)


@app.route("/emoji_id")
def emoji_id_data():
    
    # Query for the emoji data using pandas
    query_statement = db.session.query(Tourists).\
        order_by(Tourists.score.desc()).\
        limit(10).statement
    df = pd.read_sql_query(query_statement, db.session.bind)

    # Format the data for Plotly
    trace = {
        "x": df["emoji_id"].values.tolist(),
        "y": df["score"].values.tolist(),
        "type": "bar"
    }
    return jsonify(trace)


@app.route("/emoji_name")
def emoji_name_data():
    
    # Query for the top 10 emoji data
    results = db.session.query(Tourists.name, Tourists.score).\
        order_by(Tourists.score.desc()).\
        limit(10).all()
    df = pd.DataFrame(results, columns=['name', 'score'])

    # Format the data for Plotly
    plot_trace = {
        "x": df["name"].values.tolist(),
        "y": df["score"].values.tolist(),
        "type": "bar"
    }
    return jsonify(plot_trace)
"""
@app.route("/arriv_dep_data")
def tourism_arriv_dep_data():
    
    # Query for the top 10 emoji data
    # arrival_results = db.session.query (Tourists).filter(Tourists.year >= 2008, Tourists.year<=2017).\
    #     order_by(Tourists.arrivals.desc()).\
    #     limit(10).all()
    arrival_results = db.session.query (Tourists.arrivals,Tourists.country_iso,Tourists.country_name).filter(Tourists.arrivals != "").\
        filter(Tourists.year == 2017).order_by(Tourists.arrivals.desc()).\
        limit(1000).all()
    data=[]

    for arrivals, country_iso, country_name in arrival_results:
        arrival_dct = {}
        arrival_dct["arrivals"] = arrivals
        arrival_dct["country_iso"] = country_iso
        arrival_dct["country_name"] = country_name
        data.append(arrival_dct)

    return jsonify(data)

@app.route("/arrivals")
def arrivals():
    """Render Arrivals Page."""
    return render_template("test1.html")


if __name__ == '__main__':
    app.run(debug=True)
