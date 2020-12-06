

import kivy
from kivy.uix.label import Label

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
                print(destinations)
                show_popup_ans(str(destinations))
            else:
                show_popup('location does not exist')
        self.cur_location.text=""
        self.spend_time.text=""
        self.recommendations.text=""


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
    popupWin= Popup(title= "Error",
                    content= Label(text=command), size_hint= (None,None),
                    size=(400,400))
    popupWin.open()


def prepareAns(command):
    ans= command.split("\n")
    clean_ans=""
    for line in ans:
        doubleSplit= line.split("    ")
        if len(doubleSplit)>1:
            clean_ans+= doubleSplit[1] +"\n"
    return clean_ans


def show_popup_ans(ans):
    popupWin= Popup(title= "Recommended Locations",
                    content= Label(text="We recommend you to travel: \n"+ ans), size_hint= (None,None),
                    size=(400,400))
    popupWin.open()

class MyApp(App):
    def build(self):
        return MyGrid()
