# sqlalchemy-challenge

This challenge uses sqlalclchemy to help us plan a trip to Honolulu, Hawaii by doing some climate analysis.

The challenge is split into two parts

# Part 1
In this part, we use SQLAlchemy ORM queries, Pandas, and Matplotlib to look at the precipitation and temperatures at Honolulu for specified dates.

# Part 2
In this part, we create our own Flask API using the data from the queries made in the previous part.
```
There are five different routes we can use
For the precipitation results from the past 12 months use: /api/v1.0/precipitation
To get a list of all the stations use: /api/v1.0/stations
To get the dates and temperatures from the most active station use: /api/v1.0/tobs
To get the minimum temperature, the average temperature, and the maximum temperature for a specified start use: /api/v1.0/yyyy-mm-dd
To get the minimum temperature, the average temperature, and the maximum temperature for a specified start-end range. /api/v1.0/yyyy-mm-dd/yyyy-mm-dd"
```
