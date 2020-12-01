import csv
import sqlite3
import pandas as pd
import numpy as np
import datetime

class Database:
    def __init__(self):
        self.conn = sqlite3.connect('BikeShare.db')
        self.cursor = self.conn.cursor()
        self.init_db()

    def init_db(self):
        self.conn.execute(
            "CREATE TABLE IF NOT EXISTS bikeShare (TripDuration INTEGER ,StartTime DATETIME, "
            "StopTime DATETIME, StartStationID INTEGER, StartStationName TEXT, StartStationLatitude REAL,"
            " StartStationLongitude REAL, EndStationID INTEGER, EndStationName TEXT, EndStationLatitude REAL,"
            " EndStationLongitude REAL, BikeID INTEGER, UserType TEXT, BirthYear INTEGER, Gender"
            " INTEGER, TripDurationinmin INTEGER)")
        self.conn.commit()

        with open('BikeShare.csv', 'r') as f:
            reader = csv.reader(f)
            data = next(reader)
            query = 'insert into BikeShare({0}) values ({1})'
            query = query.format(','.join(data), ','.join('?' * len(data)))
            cursor = self.cursor
            for data in reader:
                cursor.execute(query, data)
            self.conn.commit()

        # execute the search query on the DB.
    def execute_query(self, start_station_name, time_duration):
        query = "SELECT * FROM bikeShare WHERE StartStationName = '" + start_station_name + "' AND TripDurationinmin <= '" + str(time_duration) + "'"
        results = self.cursor.execute(query)
        cols = [column[0] for column in results.description]
        df = pd.DataFrame.from_records(data=results.fetchall(), columns=cols)
        return df



