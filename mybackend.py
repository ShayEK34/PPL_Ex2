import csv
import sqlite3
import pandas as pd



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

    def execute_search_query_db(self, start_station_name, time_duration):
        query3 = "SELECT StartStationName,EndStationName,Num_wanted_trip,Num_wanted_destination,Trip_score,Destination_score,Destination_score*0.6+Trip_score*0.4 AS Total_score FROM (SELECT StartStationName,T1.EndStationName,Num_wanted_trip,Num_wanted_destination,(CAST(Num_wanted_trip AS DOUBLE )) / (CAST((SELECT SUM(Num_wanted_trip) AS Total_trips FROM (SELECT StartStationName,EndStationName, COUNT() AS Num_wanted_trip FROM (SELECT StartStationName,EndStationName FROM bikeShare WHERE StartStationName = '" + start_station_name + "' AND EndStationName IN (SELECT DISTINCT EndStationName FROM bikeShare WHERE StartStationName = '" + start_station_name + "' AND TripDurationinmin <= '" + str(time_duration) + "')) GROUP BY StartStationName,EndStationName ORDER BY Num_wanted_trip DESC)) AS DOUBLE )) AS Trip_score,(CAST(Num_wanted_destination AS DOUBLE )) / (CAST((SELECT SUM(Num_wanted_destination) AS Destination_score FROM (SELECT EndStationName,COUNT() AS Num_wanted_destination FROM (SELECT EndStationName FROM bikeShare) GROUP BY EndStationName ORDER BY Num_wanted_destination DESC)) AS DOUBLE )) AS Destination_score  FROM (SELECT StartStationName,EndStationName, COUNT() AS Num_wanted_trip FROM (SELECT StartStationName,EndStationName FROM bikeShare WHERE StartStationName = '" + start_station_name + "' AND EndStationName IN (SELECT DISTINCT EndStationName FROM bikeShare WHERE StartStationName = '" + start_station_name + "' AND TripDurationinmin <= '" + str(time_duration) + "')) GROUP BY StartStationName,EndStationName ORDER BY Num_wanted_trip DESC)T1 LEFT JOIN (SELECT EndStationName,COUNT() AS Num_wanted_destination FROM (SELECT EndStationName FROM bikeShare) GROUP BY EndStationName ORDER BY Num_wanted_destination DESC)T2 ON T1.EndStationName = T2.EndStationName) ORDER BY Total_score DESC "
        results = self.cursor.execute(query3)
        records = results.fetchall()
        cols = [column[0] for column in results.description]
        df = pd.DataFrame.from_records(data=records, columns=cols)
        print("1: " + str(df.shape[0]))
        return df


    def calculate_res(self, start_station_name, time_duration, num):
        results = self.execute_search_query_db(start_station_name,time_duration)
        n_results = results.head(int(num))
        destinations = n_results['EndStationName']
        destinations=self.prepareAns(destinations)
        return  destinations

    def prepareAns(self, destinations):
        return '\n'.join(destinations)

    def check_record_num(self):
        query = "SELECT * FROM bikeShare"
        results = self.cursor.execute(query)
        records = results.fetchall()
        cols = [column[0] for column in results.description]
        df = pd.DataFrame.from_records(data=records, columns=cols)
        return df.shape[0]

    def check_if_station_exist(self,start_station_name):
        query = "SELECT DISTINCT StartStationName FROM bikeShare WHERE StartStationName = '" + start_station_name + "' "
        results = self.cursor.execute(query)
        records = results.fetchall()
        cols = [column[0] for column in results.description]
        df = pd.DataFrame.from_records(data=records, columns=cols)
        is_exist = df.shape[0]
        return is_exist

