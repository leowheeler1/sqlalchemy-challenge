# Import the dependencies.
from flask import Flask # for the API
from flask import jsonify # for clean output
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func  # these are all so the database can be accessed
import numpy as np # list stuff
import datetime as dt # date objects
#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite") 
# reflect an existing database into a new model
Base = automap_base()
Base.prepare(engine)
# Save references to each table
measurement = Base.classes.measurement
station = Base.classes.station
# Create our session (link) from Python to the DB
s = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route('/') # index route
def home():
    print('landing on home page...')
    output1 = "All available routes for Hawaii Weather API:" 
    output2 = "/api/v1.0/precipitation\n - 12 Months of precipitaton data" 
    output3 = "/api/v1.0/stations\n - Info on all stations" 
    output4 = "/api/v1.0/tobs\n - Temperature info" 
    output5 = "/api/v1.0/<start> (please use yyyy-mm-dd format) - Calculates Min, Max, and Avg for all dates after start date" 
    output6 = "/api/v1.0/<start>/<end> (please use yyy-mm-dd format)\n - Calculates Min, Max, and Avg for all dates between start and end (inclusive)"
    return [output1, output2, output3, output4, output5, output6] # for some reason the response all came out on one line, this was the only way that worked to split it up 

@app.route('/api/v1.0/precipitation') # precipitaion data for last 12 months
def rain():
    outputdict = {}
    print('landing on precipitaion page...')
    sel = [measurement.date, measurement.prcp]

    firstdate = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    lastyear = s.query(*sel).filter(measurement.date >= firstdate).all()
    for row in lastyear:
        outputdict[row.date] = row.prcp
    return jsonify(outputdict)

@app.route('/api/v1.0/stations') # data on all stations
def stations():
    outputdict = {}
    print('landing on stations page...')

    stations = s.query(station)
    for row in stations:
        outputdict[row.id] = [row.station, row.name, row.latitude, row.longitude, row.elevation]
    return jsonify(outputdict)


@app.route('/api/v1.0/tobs') # temperature data from station with most observations
def tobs():
    outputdict = {}
    print('landing on tobs page...')
    sel = [measurement.date, measurement.tobs]

    output = s.query(*sel).filter(measurement.station == 'USC00519281').all() # USC00519281 is most active station
    for row in output:
        outputdict[row.date] = row.tobs
    return jsonify(outputdict)


@app.route('/api/v1.0/<start>') # data with a specific start date
@app.route('/api/v1.0/<start>/<end>') # data with specific start and end date
def custom(start = None, end = None):
    print('landing on start/end page...')
    sel = [func.min(measurement.tobs), func.max(measurement.tobs), func.avg(measurement.tobs)]

    if end == None:
        startonly = s.query(*sel).filter(measurement.date >= start).all()
        startlist = list(np.ravel(startonly))
        return jsonify(startlist)
    else:
        startandend = s.query(*sel).filter(measurement.date >= start).\
                      filter(measurement.date <= end).all()
        startandendlist = list(np.ravel(startandend))
        return jsonify(startandendlist)


if __name__ =='__main__': # debugger
    app.run(debug = True)

s.close() # always close the session