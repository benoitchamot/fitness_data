#########################################################
# Dependencies
#########################################################
from flask import Flask, jsonify
import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from sqlalchemy import desc
from pathlib import Path

#########################################################
# Functions
#########################################################

def str_to_date(in_string):
# Convert a date stored as a string from the database and convert it to a datetime object.
# Input string format: YYYY-MM-DD
    out_date = dt.datetime.strptime(in_string, '%m/%d/%Y')
    return dt.date(out_date.year, out_date.month, out_date.day)

#########################################################
# Database Setup
#########################################################

# Create engine to hawaii.sqlite
print("Connecting to database...")
db_path = Path('fitness_db.sqlite')
engine = create_engine(f"sqlite:///{db_path}")
print("Connected.")

# Reflect the database into a new model
print("Reflecting database...")
Base = automap_base()
print("Done.")

# Reflect the tables
print("Reflecting tables...")
try:
	Base.prepare(engine, reflect=True)
	print("Done.")
except Exception as inst:
    print(f"\nError: {inst}")
    print("\n*** HINT: please run script from within Server directory ***\n")
    quit()

# Save references to each table
daily_activity = Base.classes.daily_activity

#########################################################
# Flask Setup
#########################################################
app = Flask(__name__)

#########################################################
# Flask Routes
#########################################################

# Default route
@app.route("/")
def home():
	print("Server received request for Home page")
	return (
		f"<h1>Daily Activity API</h1>"
		f"<h2>Static routes</h2>"
		f"/api/v1.0/precipitation<br/>"
		f"<ul>"
		f"	<li>Returns precipitation data for the last 12 months</li>"
		f"	<li>There are multiple data points per day (multiple stations)</li>"
		f"	<li>Key: Date (string, YYYY-MM-DD)</li>"
		f"	<li>Value: Precipitation (in mm)</li>"
		f"</ul>"
		f"/api/v1.0/stations<br/>"
		f"<ul>"
		f"	<li>Returns information for all stations in the database</li>"
		f"	<li>Each station includes: id, name, latitude, longitude and elevation</li>"
		f"</ul>"
		f"/api/v1.0/tobs"
		f"<ul>"
		f"	<li>Returns temperatures for station USC00519281</li>"
		f"	<li>Data are for the last 12 months</li>"
		f"	<li>Each row includes: datetime, temperature in degC</li>"
		f"</ul>"
		f"<h2>Dynamic routes</h2>"
		f"/api/v1.0/&#x003C;start_date&#x003E;<br/>"
		f"<ul>"
		f"	<li>Returns min, max and average temperature for each date</li>"
		f"	<li>Returns value from &#x003C;start_date&#x003E to end of table</li>"
		f"	<li>Date format must be: YYYY-MM-DD</li>"
		f"</ul>"
		f"/api/v1.0/&#x003C;start_date&#x003E/&#x003C;end_date&#x003E;<br/>"
		f"<ul>"
		f"	<li>Returns min, max and average temperature for each date</li>"
		f"	<li>Returns value from &#x003C;start_date&#x003E to &#x003C;end_date&#x003E</li>"
		f"	<li>Date format must be: YYYY-MM-DD</li>"
		f"	<li>&#x003C;end_date&#x003E must be greater or equal to &#x003C;start_date&#x003E</li>"
		f"	<li>All temperatures are in degC</li>"
		f"</ul>"
	)

# Static Activity Calories route
# http://127.0.0.1:5000/api/v1.0/activities
@app.route("/api/v1.0/activities")
def api_activities():
	# Open session to the database
	session = Session(bind=engine)
	activities = session.query(daily_activity)
	
	# Create empty lists
	activities_dicts = []

	# Loop through the measurements
	for row in activities:    
    	# Add the data to a dictionary
		act_dict = {'User': row.UserId,
			  'Date': str_to_date(row.ActivityDate),
			  'Calories': row.Calories}

		# Append the data to the list of dictionary
		activities_dicts.append(act_dict)

	# Close session
	session.close()

	# Return jsonified dictionary
	return jsonify(activities_dicts)

# Dynamic User data route
@app.route("/api/v1.0/u/<user_name>")
def api_user_activities(user_name):
	# Open session to the database
	session = Session(bind=engine)
	activities = session.query(daily_activity).filter(daily_activity.UserId == user_name)

	# Create empty lists
	activities_dicts = []

	# Loop through the measurements
	for row in activities:
		# Add the data to a dictionary
		act_dict = {'ActivityDate': str_to_date(row.ActivityDate),
					'TotalSteps': row.TotalSteps,
					'TotalDistance': row.TotalDistance,
					'TrackerDistance': row.TrackerDistance,
					'LoggedActivitiesDistance': row.LoggedActivitiesDistance,
					'VeryActiveDistance': row.VeryActiveDistance,
					'ModeratelyActiveDistance': row.ModeratelyActiveDistance,
					'LightActiveDistance': row.LightActiveDistance,
					'SedentaryActiveDistance': row.SedentaryActiveDistance,
					'VeryActiveMinutes': row.VeryActiveMinutes,
					'FairlyActiveMinutes': row.FairlyActiveMinutes,
					'LightlyActiveMinutes': row.LightlyActiveMinutes,
					'SedentaryMinutes': row.SedentaryMinutes,
					'Calories': row.Calories}
		
		# Append the data to the list of dictionary
		activities_dicts.append(act_dict)

	# Close session
	session.close()

	# Return jsonified dictionary
	return jsonify(activities_dicts)

#########################################################
# Run App
#########################################################
if __name__ == "__main__":
	app.run(debug=True)
