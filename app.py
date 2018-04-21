import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


# last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
# print(last_date[0])
# last_date = last_date[0]
last_date = "2017-08-23"
one_yr_from_last_date = "2016-08-24"


@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"enter &lt;start&gt in format YYYY-MM-DD;<br/>"
        f"/api/v1.0/&lt;start&gt;<br/>"
        f"enter &lt;start&gt and &lt;end&gt in format YYYY-MM-DD;<br/>"
        f"/api/v1.0/&lt;start&gt;/&lt;end&gt;<br/>"
    )



@app.route("/api/v1.0/precipitation")
def precipitation():
    results = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date < last_date).\
        filter(Measurement.date > one_yr_from_last_date).\
        all()
    precipitation_list=list(np.ravel(results))
    return jsonify(precipitation_list)

@app.route("/api/v1.0/stations")
def stations():
    # """Return a list invoice totals by country.
    results2 = session.query(func.distinct(Measurement.station)).all()
    stations=list(np.ravel(results2))
    return jsonify(stations)
 
@app.route("/api/v1.0/tobs")   
def tobs():  
    tobs_results = session.query(Measurement.date, Measurement.tobs).\
    filter(Measurement.date < last_date).\
    filter(Measurement.date > one_yr_from_last_date).\
    all()
    
    tobs=list(np.ravel(tobs_results))

    return jsonify(tobs)

@app.route("/api/v1.0/<start>")
def start(start):
    results3 = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
    filter(Measurement.date >= start).\
    all() 

    start_date_list=list(np.ravel(results3))
    return jsonify(start_date_list)

@app.route("/api/v1.0/<start>/<end>")
def startend(start, end):
    results3 = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
    filter(Measurement.date >= start).\
    filter(Measurement.date <= end).\
    all() 

    start_end_list=list(np.ravel(results3))
    return jsonify(start_end_list)


if __name__ == '__main__':
    app.run(debug=True)
