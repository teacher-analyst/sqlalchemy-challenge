# sqlalchemy-challenge
Module 10 Challenge

This challenge has been completed in two files: the climate_starter.ipynb and app.py. Both files access the hawaii sqlite database. 

The climate starter file analyses and explores the climate data by specifically using SQLAlchemy ORM queries, Pandas and Matplotlib. First a percicipiation analysis is conducted and the results are ploted in a column graph and summary statistics are printed. Then, a station analysis is conducted. The station with the greatest number of observations is determined and lowest, highest and evrage temperature of that station are calculated. Then, a histogram is plotted of the previous 12 months of temperature observation data. 

The app.py has the design of the flask API. A connection is made to the hawaii sqlite database. An api is created that has the following routes:
/api/v1.0/precipitation
/api/v1.0/stations
/api/v1.0/tobs
/api/v1.0/<start>
/api/v1.0/<start>/<end>

The last two API's allow the input of dates which allows the user to choose the dates over which min, max and average temperature is to be caluclated and results returned. 
