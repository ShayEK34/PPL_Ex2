

import kivy
import mybackend

from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.properties import ObjectProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup


class p(FloatLayout):
    pass

class MyGrid(GridLayout):
    cur_location= ObjectProperty(None)
    spend_time= ObjectProperty(None)
    recommendations= ObjectProperty(None)

    def btn(self):
        self.db = mybackend.Database()

        print(str(self.cur_location.text), 'cur_location')
        print(str(self.spend_time.text), 'spend_time')
        print(str(self.recommendations.text), 'recommendations')

        if self.valid_values():
            ans= self.db.check_if_station_exist(self.cur_location.text)
            if ans==1:
                destinations= self.db.calculate_res(self.cur_location.text,self.spend_time.text, self.recommendations.text)
                show_popup(str(destinations))
            else:
                show_popup('location does not exist')
        self.cur_location= ""
        self.spend_time= ""
        self.recommendations.text= ""


    def valid_values(self):
        try:
            if not isinstance(self.cur_location.text, str):
                show_popup('location is not valid')
                return False

            if not isinstance(int(self.spend_time.text), int):
                show_popup('spend time is not valid')
                return False

            if not isinstance(int(self.recommendations.text), int):
                show_popup('recommendations is not valid')
                return False

            return True
        except:
            return False

def show_popup(command):
    show= p()

    popupWin= Popup(title= command, content= show, size_hint= (None,None),
                    size=(400,400))

    popupWin.open()


class MyApp(App):
    def build(self):
        return MyGrid()
