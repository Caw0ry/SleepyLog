from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.pagelayout import PageLayout
from kivy.uix.scrollview import ScrollView
from kivy.metrics import dp

class SleepyLog(App):
    def build(self):
        lb = Label(
            text = "A",
            font_size = 100,

        )
        bt1 = Button(
            text = "1",
            font_size = 40,
            size = (dp(100), dp(100))

        )
        bt2 = Button(
            text = "2",
            font_size = 40,
            size = (dp(100), dp(100))
        )
        bt3 = Button(
            text = "3",
            font_size = 40,
            size = (dp(100), dp(100))
        )
        gl = GridLayout(
            cols = 3,
            rows = 1,
            size_hint = [1, 0.08]

        )

        bl = BoxLayout(
            orientation = 'vertical',

        )

        bl.add_widget(lb)
        gl.add_widget(bt1)
        gl.add_widget(bt2)
        gl.add_widget(bt3)
        bl.add_widget(gl)
        
        
        return bl
    
if __name__ == '__main__':
    SleepyLog().run()