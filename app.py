# Import the dependencies.
from flask import Flask, jsonify

import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect


#################################################
# Database Setup
#################################################


# reflect an existing database into a new model
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
# reflect the tables
Base = automap_base()
Base.prepare(autoload_with=engine)

# Save references to each table
measurement = Base.classes.measurement
station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(bind = engine)

#################################################
# Flask Setup
#################################################

app = Flask(__name__)




#################################################
# Flask Routes
#################################################

@app.route("/")
def home():
    return (
        f"<h1> Available Routes:</h1>"
        f"For the precipitation results from the past 12 months use: /api/v1.0/precipitation<br/>"
        f"To get a list of all the stations use: /api/v1.0/stations<br/>"
        f"To get the dates and temperatures from the most active station use: /api/v1.0/tobs<br/>"
        f"To get the minimum temperature, the average temperature, and the maximum temperature for a specified start use: /api/v1.0/yyyy-mm-dd<br/>"
        f"To get the minimum temperature, the average temperature, and the maximum temperature for a specified start-end range. /api/v1.0/yyyy-mm-dd/yyyy-mm-dd"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():

    session = Session(engine)

    query_date = dt.date(2017, 8, 23) - dt.timedelta(days=365) 
    rain_info = session.query(measurement.date,measurement.prcp).\
        filter(func.strftime(measurement.date) >= query_date).all()
    
    session.close()

    output = []
    for date, percipitation in rain_info:
        rain_dict = {}
        rain_dict["date"] = date
        rain_dict["percipitation"] = percipitation
        output.append(rain_dict)
    
    return jsonify(output)

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)

    stations_info = session.query(station.station).all()
    
    session.close()

    stations_list = []
     
    for i in stations_info:
        stations_list.append(i[0])

    return jsonify(stations_list)


@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)

    query_date = dt.date(2017, 8, 23) - dt.timedelta(days=365) 
    station_query = session.query(measurement.station,func.count(measurement.station))\
    .group_by(measurement.station)\
    .order_by(func.count(measurement.station).desc()).all()

    most_active = station_query[0][0]

    most_active_data = session.query(measurement.date,measurement.tobs).filter(measurement.station == most_active).\
        filter(func.strftime(measurement.date) >= query_date).all()
    
    session.close()

    output = []
    for date, temperature in most_active_data:
        temp_dict = {}
        temp_dict["date"] = date
        temp_dict["temperature"] = temperature
        output.append(temp_dict)
    
    return jsonify(output)

@app.route("/api/v1.0/<start>")
def stats_start(start):
    session = Session(engine)

    query_data = session.query(func.min(measurement.tobs),\
            func.max(measurement.tobs),\
            func.avg(measurement.tobs))\
            .filter(measurement.date >= start ).all()
    
    session.close()

    output = []

    for min, max, avg in query_data:
        temp_dict = {}
        temp_dict['Min'] = min
        temp_dict['Max'] = max
        temp_dict['Avg'] = avg
        output.append(temp_dict)
    
    return jsonify(output)

@app.route("/api/v1.0/<start>/<end>")
def stats_end(start,end):
    session = Session(engine)

    query_data = session.query(func.min(measurement.tobs),\
            func.max(measurement.tobs),\
            func.avg(measurement.tobs))\
            .filter(measurement.date >= start )\
            .filter(measurement.date <= end ).all()
    
    session.close()

    output = []

    for min, max, avg in query_data:
        temp_dict = {}
        temp_dict['Min'] = min
        temp_dict['Max'] = max
        temp_dict['Avg'] = avg
        output.append(temp_dict)
    
    return jsonify(output)


if __name__ == '__main__': 
    app.run(debug=False)

