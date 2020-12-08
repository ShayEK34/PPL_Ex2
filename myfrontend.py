

import kivy
from kivy.uix.label import Label

import mybackend

from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.properties import ObjectProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy.core.audio import SoundLoader

"""
class p represents the pop up window
"""
class p(FloatLayout):
    pass

"""
class MyGrid is the main page of the desktop application 
"""
class MyGrid(GridLayout):
    """
    binding to .kv elemnts
    """
    cur_location = ObjectProperty(None)
    spend_time = ObjectProperty(None)
    recommendations = ObjectProperty(None)

    """
    btn function- activate when the user ask for recommendations
    """
    def btn(self):
        if valid_values(self):
            # activate the music when the user ask for recommendations
            try:
                if(self.music.status=='play'):
                    pass
            except:
                self.music = SoundLoader.load('Queen-Bicycle.wav')
                self.music.play()

            self.db = mybackend.Database()
            ans= self.db.check_if_station_exist(self.cur_location.text)
            if ans==1:    # ans==1 means there is an answer
                destinations= self.db.calculate_res(self.cur_location.text,self.spend_time.text, self.recommendations.text)
                # if there are less recommendations founded
                if(len(destinations.split('\n'))<(int)(self.recommendations.text)):
                    show_popup_ans("\nwe found only "+str(len(destinations.split('\n')))+" places to travel: \n"+str(destinations))
                else:
                    show_popup_ans(str(destinations))
            else:   # ans==0 means there is no relevant answer
                show_popup('location does not exist in the db')

        self.cur_location.text=""
        self.spend_time.text=""
        self.recommendations.text=""


"""
check if the param input is consists only of number 
"""
def only_numbers(param):
    return all(char.isdigit() for char in param)

"""
check valid values
check if inputs not empty  and if valid by the rules
"""
def valid_values(self):
    try:
        if self.cur_location.text=='':
            show_popup('location should not by empty')
            return False
        if only_numbers(self.cur_location.text):
            show_popup('location can not be only numbers')
            return False
        if self.spend_time.text == '':
            show_popup('spend time should not by empty')
            return False
        if not only_numbers(self.spend_time.text):
            show_popup('spend time is not valid')
            return False
        if self.recommendations.text == '':
            show_popup('recommendations should not by empty')
            return False
        if not only_numbers(self.recommendations.text):
            show_popup('recommendations is not valid')
            return False
        return True
    except:
        return False

"""
create pop up win with an error
"""
def show_popup(command):
    popupWin= Popup(title= "Error",
                    content= Label(text=command), size_hint= (None,None),
                    size=(400,400))
    popupWin.open()

"""
create pop up win with answer
"""
def show_popup_ans(ans):
    popupWin= Popup(title= "Recommended Locations",
                    content= Label(text="We recommend you to travel: \n"+ ans), size_hint= (None,None),
                    size=(400,400))
    popupWin.open()

class MyApp(App):
    def build(self):
        return MyGrid()


if __name__ == '__main__':
    MyApp().run()

