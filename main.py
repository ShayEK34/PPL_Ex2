import time

import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout


class MyApp(App):
    def build(self):
        return Label(text="Our first app")




# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    MyApp().run()
    # time_start_logreg = time.time()
    # db = mybackend.Database()
    # print(db)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
