import time
from myfrontend import *

import kivy
import mybackend
import myfrontend


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # MyApp().run()
    # time_start_logreg = time.time()
    db = mybackend.Database()
    # db.execute_search_query2("City Hall",20)
    db.check_if_station_exist("City Call")
    db.calculate_res("City Hall",2,6)
    # print(db)

