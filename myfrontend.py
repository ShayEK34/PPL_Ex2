

import kivy
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput

class MyGrid(GridLayout):
    def __init__(self, **kwargs):
        super(MyGrid, self).__init__(**kwargs)
        self.cols=1

        self.in_grid= GridLayout()
        self.in_grid.cols=2
        self.in_grid.add_widget(Label(text="what is your current location?"))
        self.cur_location= TextInput(multiline= False)
        self.in_grid.add_widget( self.cur_location)
        self.in_grid.add_widget(Label(text="How much time would you like to spend?"))
        self.spend_time = TextInput(multiline=False)
        self.in_grid.add_widget(self.spend_time)
        self.in_grid.add_widget(Label(text="How much location recommendations would you like to receive?"))
        self.recommendations = TextInput(multiline=False)
        self.in_grid.add_widget(self.recommendations)

        self.add_widget(self.in_grid)
        self.submit= Button(text="Submit", font_size=40)
        self.add_widget( self.submit)
        self.submit.bind(on_press= self.clicked)


    def clicked(self, instance):
        cur_location= self.cur_location.text
        spend_time = self.spend_time.text
        recommendations= self.recommendations.text

        self.cur_location= ""
        self.spend_time= ""
        self.recommendations.text= ""

class MyApp(App):
    def build(self):
        return MyGrid()
