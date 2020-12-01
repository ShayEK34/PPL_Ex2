import csv
import operator
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
        num_records = self.check_record_num()
        if num_records == 0:
            self.insert_values()

    def insert_values(self):
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

    def execute_search_query(self, start_station_name, time_duration):
        query = "SELECT * FROM bikeShare WHERE StartStationName = '" + start_station_name + "' AND TripDurationinmin <= '" + str(time_duration) + "'"
        results = self.cursor.execute(query)
        records = results.fetchall()
        cols = [column[0] for column in results.description]
        df = pd.DataFrame.from_records(data=records, columns=cols)
        print("1: " + str(df.shape[0]))
        return df

    def extract_end_stations(self, start_station_name, time_duration):
        query = "SELECT DISTINCT EndStationName FROM bikeShare WHERE StartStationName = '" + start_station_name + "' AND TripDurationinmin <= '" + str(
            time_duration) + "'"
        results = self.cursor.execute(query)
        cols = [column[0] for column in results.description]
        df = pd.DataFrame.from_records(data=results.fetchall(), columns=cols)
        return df

    def calculate_res(self, start_station_name, time_duration, num):
        all_values = self.extract_all_data()
        end_stations = self.extract_end_stations(start_station_name, time_duration)
        # all_filterd_results = self.execute_search_query(start_station_name, time_duration)
        dict = self.count_end_stations(end_stations, all_values)
        print(dict)
        dict2 = self.count_trip_ways(start_station_name,end_stations, all_values)
        print(dict2)


    def count_end_stations(self, end_stations, all_first_results):
        end_stations_count = {}
        for station in end_stations.values:
            station_val = station[0]
            seriesObj = all_first_results.apply(lambda x: True if x['EndStationName'] == station_val else False, axis=1)
            # Count number of True in series
            numOfRows = len(seriesObj[seriesObj == True].index)
            end_stations_count[station_val] = numOfRows
        sorted_end_stations_count = dict(sorted(end_stations_count.items(),key=operator.itemgetter(1), reverse=True))
        return sorted_end_stations_count

    def check_record_num(self):
        query = "SELECT * FROM bikeShare"
        results = self.cursor.execute(query)
        records = results.fetchall()
        cols = [column[0] for column in results.description]
        df = pd.DataFrame.from_records(data=records, columns=cols)
        return df.shape[0]

    def count_trip_ways(self, start_station_name, end_stations, all_first_results):
        trip_count = {}
        for station in end_stations.values:
            station_val = station[0]
            seriesObj = all_first_results.apply(lambda x: True if x['StartStationName'] == start_station_name and x['EndStationName'] == station_val else False, axis=1)
            # Count number of True in series
            numOfRows = len(seriesObj[seriesObj == True].index)
            trip_count[station_val] = numOfRows
        sorted_trip_count = dict(sorted(trip_count.items(), key=operator.itemgetter(1), reverse=True))
        return sorted_trip_count

    def extract_all_data(self):
        query = "SELECT * FROM bikeShare"
        results = self.cursor.execute(query)
        records = results.fetchall()
        cols = [column[0] for column in results.description]
        all_data = pd.DataFrame.from_records(data=records, columns=cols)
        return all_data
