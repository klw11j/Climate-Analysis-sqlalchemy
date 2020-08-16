import numpy as np
import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt
from flask import Flask, jsonify

#################################################
# Database Setup
#################################################

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base = automap_base()
Base.prepare(engine, reflect=True)

measurement = Base.classes.measurement 
station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################


@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"

    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    last_year = dt.date(2017,8,23)-dt.timedelta(days=365)
    query_date = session.query(measurement.date, measurement.prcp).filter(measurement.date>=last_year).all()

    session.close()

    percip_date=[]
    for date, prcp in query_date:
        percip_date_dict ={}
        percip_date_dict[date]= prcp
        percip_date.append(percip_date_dict)

    return jsonify(percip_date)
    

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    station_query = session.query(station.station, station.name).all()
    session.close()

    station_name=[]
    for station, name in station_query:
        station_name_dict={}
        station_name_dict[station]= name
        station_name.append(station_name_dict)                  

    return jsonify(station_name)


if __name__ == '__main__':
    app.run(debug=True)