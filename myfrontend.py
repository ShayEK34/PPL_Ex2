

import kivy
from kivy.uix.label import Label

import mybackend

from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.properties import ObjectProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy.animation import Animation
from kivy.core.audio import SoundLoader
from kivy.uix.switch import Switch

class p(FloatLayout):
    pass


class MyGrid(GridLayout):
    cur_location = ObjectProperty(None)
    spend_time = ObjectProperty(None)
    recommendations = ObjectProperty(None)

    # def switch_callback(self, switchObject, switchValue):
    #
    #     # Switch value are True and False
    #     if (switchValue):
    #         print('Switch is ON:):):)')
    #     else:
    #         print('Switch is OFF:(:(:(')

    def btn(self):
        # print(str(self.cur_location.text), 'cur_location')
        # print(str(self.spend_time.text), 'spend_time')
        # print(str(self.recommendations.text), 'recommendations')

        if valid_values(self):
            music = SoundLoader.load('Queen-Bicycle.wav')
            if music:
                music.play()
            prep_location=prepare_data(self.cur_location.text)
            self.db = mybackend.Database()
            ans= self.db.check_if_station_exist(prep_location)
            if ans==1:
                destinations= self.db.calculate_res(prep_location,self.spend_time.text, self.recommendations.text)
                if(len(destinations.split('\n'))<(int)(self.recommendations.text)):
                    show_popup_ans("\nwe found only "+str(len(destinations.split('\n')))+" places to travel: \n"+str(destinations))
                else:
                    show_popup_ans(str(destinations))
            else:
                show_popup('location does not exist in the db')

        self.cur_location.text=""
        self.spend_time.text=""
        self.recommendations.text=""

    def animate(self):
        # create an animation object. This object could be stored
        # and reused each call or reused across different widgets.
        # += is a sequential step, while &= is in parallel
        animation = Animation(pos=(100, 100), t='out_bounce')
        animation += Animation(pos=(200, 100), t='out_bounce')
        animation &= Animation(size=(500, 500))
        animation += Animation(size=(100, 50))

        # apply the animation on the button, passed in the "instance" argument
        # Notice that default 'click' animation (changing the button
        # color while the mouse is down) is unchanged.
        animation.start(self)


def prepare_data(location):
    ans=""
    if ' ' in location:
        location_array= location.split(' ')
        for word in location_array:
            if ans=="":
                ans= ans + word.capitalize()
            else:
                ans= ans+' '+ word.capitalize()
    return ans


def only_alpha(param):
    if ' ' in param:
        params_array= param.split(' ')
        if ' ' in params_array:
            params_array.remove(' ')
        return all(word.isalpha() for word in params_array)
    return param.isalpha()


def only_numbers(param):
    return all(char.isdigit() for char in param)


def valid_values(self):
    try:
        if self.cur_location.text=='':
            show_popup('location should not by empty')
            return False
        if not only_alpha(self.cur_location.text):
            show_popup('location should consist of letters only')
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


def show_popup(command):
    popupWin= Popup(title= "Error",
                    content= Label(text=command), size_hint= (None,None),
                    size=(400,400))
    popupWin.open()


def show_popup_ans(ans):
    popupWin= Popup(title= "Recommended Locations",
                    content= Label(text="We recommend you to travel: \n"+ ans), size_hint= (None,None),
                    size=(400,400))
    popupWin.open()

class MyApp(App):
    def build(self):
        return MyGrid()
