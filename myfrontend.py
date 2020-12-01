

import kivy
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.properties import ObjectProperty
from kivy.core.window import Window

class MyGrid(GridLayout):
    # Window.clearcolor=(1,1,1,1)
    cur_location= ObjectProperty(None)
    spend_time= ObjectProperty(None)
    recommendations= ObjectProperty(None)

    def btn(self):

        print(self.cur_location.text, 'cur_location')
        print(self.spend_time.text, 'spend_time')
        print(self.recommendations.text, 'recommendations')

        self.cur_location= ""
        self.spend_time= ""
        self.recommendations.text= ""

    # def __init__(self, **kwargs):
    #     super(MyGrid, self).__init__(**kwargs)
    #     self.cols=1
    #
    #     self.in_grid= GridLayout()
    #     self.in_grid.cols=2
    #     self.in_grid.add_widget(Label(text="what is your current location?"))
    #     self.cur_location= TextInput(multiline= False)
    #     self.in_grid.add_widget( self.cur_location)
    #     self.in_grid.add_widget(Label(text="How much time would you like to spend?"))
    #     self.spend_time = TextInput(multiline=False)
    #     self.in_grid.add_widget(self.spend_time)
    #     self.in_grid.add_widget(Label(text="How much location recommendations would you like to receive?"))
    #     self.recommendations = TextInput(multiline=False)
    #     self.in_grid.add_widget(self.recommendations)
    #
    #     self.add_widget(self.in_grid)
    #     self.submit= Button(text="Submit", font_size=40)
    #     self.add_widget( self.submit)
    #     self.submit.bind(on_press= self.clicked)





class MyApp(App):
    def build(self):
        return MyGrid()
