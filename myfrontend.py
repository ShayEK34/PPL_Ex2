

import kivy
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

        print(str(self.cur_location.text), 'cur_location')
        print(str(self.spend_time.text), 'spend_time')
        print(str(self.recommendations.text), 'recommendations')

        self.cur_location= ""
        self.spend_time= ""
        self.recommendations.text= ""

        show_popup()

def show_popup():
    show= p()

    popupWin= Popup(title= "hi", content= show, size_hint= (None,None),
                    size=(400,400))

    popupWin.open()


class MyApp(App):
    def build(self):
        return MyGrid()
