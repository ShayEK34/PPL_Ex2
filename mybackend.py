import csv
import sqlite3
import pandas as pd


"""
This class represent a DataBase that create SQL-Lite DB 
that contains different bike trips in NYC. 
"""
class Database:
    """
    This constructor create a SQL-Lite data-base in name BikeShare than we open connection to this DB and insert values
    from given csv file.
    """
    def __init__(self):
        self.conn = sqlite3.connect('BikeShare.db')
        self.cursor = self.conn.cursor()
        self.initial_db()

    """
    This function read a given csv file to dataframe, remove duplicates values, create table in name "BikeShare" 
    and insert all the data from the dataframe to the table.
    if the table already exist it's not create the table again catch the exception and continue to run the program. 
    """
    def initial_db(self):
        data = pd.read_csv('BikeShare.csv')
        data_duplicates_removed = pd.DataFrame.drop_duplicates(data)
        try:
            data_duplicates_removed.to_sql(name='BikeShare',con=self.conn, if_exists='fail', index=False)
        except ValueError as err:
            pass

    """
    This function execute a query algorithm on the Database that that give a score to each bike trip in NYC in the given.
    """
    def execute_search_query_db(self, start_station_name, time_duration):
        query = "SELECT StartStationName,EndStationName,Num_wanted_trip,Num_wanted_destination,Trip_score,Destination_score,"\
                 "Destination_score*0.6+Trip_score*0.4 AS Total_score FROM "\
                 " (SELECT StartStationName,T1.EndStationName,Num_wanted_trip,Num_wanted_destination,"\
                 "(CAST(Num_wanted_trip AS DOUBLE )) / (CAST((SELECT SUM(Num_wanted_trip) AS Total_trips FROM "\
                 "(SELECT StartStationName,EndStationName, COUNT() AS Num_wanted_trip FROM "\
                 " (SELECT StartStationName,EndStationName FROM bikeShare"\
                 " WHERE StartStationName = '" + start_station_name + "' AND EndStationName IN "\
                 "(SELECT DISTINCT EndStationName FROM bikeShare "\
                 " WHERE StartStationName = '" + start_station_name + "' AND TripDurationinmin <= '" + str(time_duration) + "'))"\
                 " GROUP BY StartStationName,EndStationName ORDER BY Num_wanted_trip DESC)) AS DOUBLE )) AS Trip_score,"\
                 "(CAST(Num_wanted_destination AS DOUBLE )) / (CAST((SELECT SUM(Num_wanted_destination) AS Destination_score"\
                 " FROM (SELECT EndStationName,COUNT() AS Num_wanted_destination FROM (SELECT EndStationName FROM bikeShare)"\
                 " GROUP BY EndStationName ORDER BY Num_wanted_destination DESC)) AS DOUBLE )) AS Destination_score  "\
                 " FROM (SELECT StartStationName,EndStationName, COUNT() AS Num_wanted_trip FROM "\
                 " (SELECT StartStationName,EndStationName FROM bikeShare WHERE StartStationName = '" + start_station_name + "' "\
                 " AND EndStationName IN (SELECT DISTINCT EndStationName FROM bikeShare "\
                 " WHERE StartStationName = '" + start_station_name + "' AND TripDurationinmin <= '" + str(time_duration) + "')) "\
                 " GROUP BY StartStationName,EndStationName ORDER BY Num_wanted_trip DESC)T1 "\
                 " LEFT JOIN (SELECT EndStationName,COUNT() AS Num_wanted_destination FROM (SELECT EndStationName FROM bikeShare) "\
                 " GROUP BY EndStationName ORDER BY Num_wanted_destination DESC)T2 ON T1.EndStationName = T2.EndStationName) "\
                 " ORDER BY Total_score DESC "

        results = self.cursor.execute(query)
        records = results.fetchall()
        cols = [column[0] for column in results.description]
        data = pd.DataFrame.from_records(data=records, columns=cols)
        # print("1: " + str(data.shape[0]))
        return data

    """
    This function get the start station name, trip time duration and the number of recommendations that the user want 
    to get and return the the best recommendations by the user request.
    """
    def calculate_res(self, start_station_name, time_duration, num):
        results = self.execute_search_query_db(start_station_name,time_duration)
        if(len(results)==0):
            start_station_name = self.prepare_data(start_station_name)
            results = self.execute_search_query_db(start_station_name, time_duration)
        if(len(results)<int(num)):
            n_results = results.head(len(results))
        else:
            n_results = results.head(int(num))
        destinations = n_results['EndStationName']
        destinations=self.prepareAns(destinations)
        return  destinations

    """
    This function concatenate the given destination results in one sentence 
    """
    def prepareAns(self, destinations):
        return '\n'.join(destinations)

    """
    This function check if the given start station name appearance in the database.
    """
    def check_if_station_exist(self,start_station_name):
        query = "SELECT DISTINCT StartStationName FROM bikeShare WHERE StartStationName = '" + start_station_name + "' "
        results = self.cursor.execute(query)
        records = results.fetchall()
        if(len(records)==0):
            start_station_name = self.prepare_data(start_station_name)
            query = "SELECT DISTINCT StartStationName FROM bikeShare WHERE StartStationName = '" + start_station_name + "' "
            results = self.cursor.execute(query)
            records = results.fetchall()
        cols = [column[0] for column in results.description]
        df = pd.DataFrame.from_records(data=records, columns=cols)
        is_exist = df.shape[0]
        return is_exist

    """
    This function change the location fotmat,
    it replace every start letter in the word to capital
    because most of the data is represents in that way
    """
    def prepare_data(self,location):
        ans = ""
        if ' ' in location:
            location_array = location.split(' ')
            for word in location_array:
                if ans == "":
                    ans = ans + word.capitalize()
                else:
                    ans = ans + ' ' + word.capitalize()
        return ans
