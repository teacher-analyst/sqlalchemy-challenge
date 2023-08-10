#import libraries
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt


from flask import Flask, jsonify

#Database setup

engine=create_engine("sqlite:///Resources/hawaii.sqlite")

#reflect an existing database into a new model
Base = automap_base()

#reflect the tables
Base.prepare(autoload_with = engine)

#save reference to each table
Measurement = Base.classes.measurement
Station = Base.classes.station 

#set session variable 
session = Session(engine)

#Flask setup

app=Flask(__name__)

#Flask Routes

@app.route("/")
def homepage():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/startdate<br/>"
        f"/api/v1.0/startdate/enddate<br/>"
        f"<br/>"
        f"If you would like to return average, min and max temperature values for a specific date, enter a start date or start and end date in the format YYYY-MM-DD."
    )

#precipitation route

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB

    """Return a list of precipitation data for each date"""
    # Query date and precipitation values
    results = session.query(Measurement.date, Measurement.prcp).all()

    session.close()

    # Convert list of tuples into normal list
    all_measurements = list(np.ravel(results))

    return jsonify(all_measurements)

#station route

@app.route("/api/v1.0/stations")
def station():
    # Create our session (link) from Python to the DB

    """Return a list of all stations"""
    # Query stations in the datatabse
    results = session.query(Station.station).all()

    session.close()

    all_stations = list(np.ravel(results))

    return jsonify(all_stations)

    
#tobs route
@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB

    """Return a list of data for the most active station for the last year"""
    # Query stations in the datatabse
    results = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.station == "USC00519281").\
        filter(Measurement.date >= '2016-08-23').\
        filter(Measurement.date <= '2017-08-23').all()
    
    session.close()

    tobs_station = list(np.ravel(results))

    return jsonify(tobs_station)

#Temperature route which accepts a start date or start and end date
@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")


def start_temp(start,end=None):
    #if only start date in entered in the API URL
    if not end:
        sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
        #start and date format is set to YYYY-MM-DD
        start=dt.datetime.strptime(start, "%Y-%m-%d")

        results = session.query(*sel).\
            filter(Measurement.date >= start).all()

        session.close()
    
        temp = list(np.ravel(results))

        return jsonify(temp)
    
    #if start and end date are entered in the API URL
    if start and end:
        sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
        end=dt.datetime.strptime(end, "%Y-%m-%d")
        start=dt.datetime.strptime(start, "%Y-%m-%d")
        
        results = session.query(*sel).\
            filter(Measurement.date >= start).filter(Measurement.date <=end).all()

        session.close()

        temp1 = list(np.ravel(results))

        return jsonify(temp1)

if __name__ == '__main__':
    app.run(debug=True)
