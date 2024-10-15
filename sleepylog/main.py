from datetime import date, timedelta, datetime
import math
import os
import re

from kivy.app import App
from kivymd.app import MDApp
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
from kivy.properties import BooleanProperty, NumericProperty
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.pagelayout import PageLayout
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
from kivymd.uix.button import MDButton
from kivymd.uix.button import MDButtonText
from kivy.core.window import Window
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.metrics import dp
from kivy.graphics import Color, Rectangle
import json

class ClockLayout(FloatLayout):
    """"""


class ClockTimeBgLayout(FloatLayout):
    """"""


class InputLayout(FloatLayout):
    """"""


class NoAlarmLabel(Label):
    """"""


class SetAlarmLayout(FloatLayout):
    """"""


class TimeLayout(FloatLayout):
    """"""


class TimeWid(Widget):
    """"""


class GeneralLayout(PageLayout):
    time = ObjectProperty(datetime.now())

    def __init__(self, **kwargs):
        Clock.schedule_interval(
            self.update_time, 1
        )
        super().__init__(**kwargs)

    def update_time(self, dt):
        self.time = datetime.now()
        return True


class Alarm(Widget):
    alarm_time = StringProperty()
    playing = BooleanProperty(False)
    sound = ObjectProperty(
        SoundLoader.load(
            os.path.join('alarm-sounds', 'sound1.wav'),
        )
    )

    def __init__(self, **kwargs):
        self.check = Clock.schedule_interval(self.time_check, 1)
        self.sound.loop = True
        super().__init__(**kwargs)

    def to_datetime(self, value):
        time = self.parent.parent.time
        x = datetime.strptime(value, r'%H:%M:%S')
        x = datetime(time.year, time.month, time.day, x.hour, x.minute, x.second)
        return x

    def time_check(self, dt):
        alarm_time_dt = self.to_datetime(self.alarm_time)
        if (alarm_time_dt - timedelta(seconds=1) <= 
        self.parent.parent.time <= alarm_time_dt + 
        timedelta(seconds=1)) and not self.playing:
            self.playing = True
            self.sound.play()
            Clock.schedule_once(
                self.remove, 60
            )

    def remove(self, *args):
        if self.playing:
            self.sound.stop()
        self.check.cancel()
        self.parent.remove_widget(self)


class AlarmInput(TextInput):
    def __init__(self, **kwargs):
        self.h_patt = re.compile(r'^(([0-1][0-9])|(2[0-3]))$')
        self.m_patt = re.compile(r'^([0-5][0-9])$')
        self.s_patt = self.m_patt
        super().__init__(**kwargs)
   
    def clear_text(self):
        Clock.schedule_once(
            lambda _: setattr(
                self, 'text', ''
            )
        )

    def add_colon(self):
        Clock.schedule_once(
            lambda _: setattr(
                self, 'text', str(self.text) + ':'
                )
            )

    def move_cursor_colon(self):
        Clock.schedule_once(
            lambda _: setattr(
                self, 'cursor', (self.cursor[0]+1, self.cursor[1])
                )
            )

    def keyboard_on_key_down(self, window, keycode, text, modifiers):

        if len(self.text) == 8:
            if keycode[1] == 'enter':
                alarms_lay = self.parent.parent.parent.children[1]
                try:
                    if len(alarms_lay.children) < 8:
                        alarms_lay.add_widget(
                            Alarm(alarm_time=self.text)
                        )
                except IndexError:
                    alarms_lay.add_widget(Alarm(alarm_time=self.text))
                self.clear_text()
                Clock.schedule_once(
                    lambda _: setattr(
                        self, 'focus', False
                    )
                )
            elif keycode[1] == 'backspace':
                self.clear_text()
            Clock.schedule_once(
            lambda _: setattr(
                self, 'text', self.text[:-1]
                )
            )
            return True
        for c in keycode[1]:  
            if c.isdigit():
                return super().keyboard_on_key_down(window, keycode, text, modifiers)
        self.clear_text()
        return True


    def on_text(self, instance, value):
        length = len(self.text)
        if length == 2:
            if self.h_patt.match(self.text):
                self.add_colon()
                self.move_cursor_colon()
                return True    
            self.clear_text()
            return True
        elif length == 5:
            mins = self.text[-2:]
            if self.m_patt.match(mins):
                self.add_colon()
                self.move_cursor_colon()
                return True
            self.clear_text()
            return True
        elif length == 8:
            secs = self.text[-2:]
            if self.m_patt.match(secs):
                return True
            self.clear_text()
            return True


class AlarmsLayout(BoxLayout):
    label = ObjectProperty()

    def __init__(self, **kwargs):
        Clock.schedule_interval(self.check_if_alarms, 0.05)
        super().__init__(**kwargs)

    def check_if_alarms(self, dt):
        if not self.label and not self.children:
            self.label = NoAlarmLabel()
            self.add_widget(self.label)
        elif self.label and len(self.children) > 1:
            self.remove_widget(self.label)
            self.label = ''


class ClockWid(Widget):
    h_degrees = NumericProperty()
    m_degrees = NumericProperty()
    s_degrees = NumericProperty()

    def __init__(self, **kwargs):
        self.clock = Clock.schedule_interval(self.set_degrees, 1)
        super().__init__(**kwargs)
        
    def angle(self, pointer: str):
        now = self.parent.parent.parent.time
        if pointer == 'hour':
            segs = (now.hour%12)*60*60 + now.minute*60 + now.second
            return math.radians((360/(12*60*60))*segs)
        elif pointer == 'minute':
            segs = now.minute*60 + now.second
            return math.radians((360/(60*60))*segs)
        elif pointer == 'second':
            return math.radians((360/60)*now.second)

    def set_degrees(self, dt):
        self.h_degrees = self.angle('hour')
        self.m_degrees = self.angle('minute')
        self.s_degrees = self.angle('second')
        return True
     
class ti_1(TextInput):
    def on_text(self, instance, value):
        try:
            if int(value) > 23:
                instance.text = str(23)
        except ValueError:
                pass
        
class ti_2(TextInput):
    def on_text(self, instance, value):
        try:
            if int(value) > 59:
                instance.text = str(59)
        except ValueError:
            pass

class BX(BoxLayout):
    """"""
class SV(ScrollView):
    """"""

class SleepyLogApp(MDApp):
    def build(self):
        #Функция перебора дат
        def daterange(start_date, end_date):
            for n in range(int((end_date - start_date).days)):
                yield start_date + timedelta(n)
        start_date = date(2024, 5, 1)
        end_date = date(2024, 6, 1)
        #Настройка экрана
        Window.clearcolor = [24/255,2/255,78/255,1]
        bl0 = BX()
        #Метод ScrollView
        sv =SV()
        bl0.bind(minimum_height=bl0.setter('height'))
        #Кнопка сохранения
        bt = MDButton(
            MDButtonText(
                text = "SAVE",
                theme_text_color = 'Custom',
                text_color = [127/255,255/255,212/255,1],
                font_style = 'Title',
                theme_font_size = 'Custom',
                font_size = 180,
                pos_hint = {'center_x':0.5,'center_y':0.5}
            ),
            style = 'elevated',
            radius = [dp(0),dp(0),dp(0),dp(0)],
            md_bg_color = [24/255,2/255,78/255,1],
            md_bg_color_disabled = [24/255,2/255,78/255,1],
            theme_height = 'Custom',
            theme_width = 'Custom',
            theme_bg_color = 'Custom',
            size_hint = [1,None],
            height = 180
        )
        bt.bind(on_press=self.save_data)
        #Массивы с текстовыми полями
        self.til1 = []
        self.til2 = []
        self.til3 = []
        self.til4 = []
        for i in daterange(start_date,end_date):
            glv = GridLayout(
                cols = 2,
                size_hint = [1, None],
                height = 200,
                spacing = 100
            )
            #Создание блоков с текстовыми полями
            bl1 = BoxLayout(
                orientation = 'horizontal',
                size_hint = [None,None],
                height = 200,
                width = 500,
                spacing = 0,
            )
            bl2 = BoxLayout(
                orientation = 'horizontal',
                size_hint = [None,None],
                height = 200,
                width = 500,
                spacing = 0,
            )
            #БЛОК1
            ti1 = ti_1(
                font_size = 150,
                background_color = [24/255,2/255,78/255,0],
                cursor_color = [127/255,255/255,212/255,0.5],
                foreground_color = [127/255,255/255,212/255,0.5],
                input_filter = 'int',
                multiline = False,
                hint_text = "00",
                hint_text_color = [127/255,255/255,212/255,0.5],
                size_hint = [None,None],
                height = 200,
                width = 180,
            )
            self.til1.append(ti1)
            bl1.add_widget(ti1)
            lbc1 = Label(
                text = ":",
                color = [127/255,255/255,212/255,0.5],
                font_size = 150,
                size_hint = [None,None],
                height = 230,
                width = 100,
                valign = 'top',
                halign = 'center',
            )
            bl1.add_widget(lbc1)
            ti2 = ti_2(
                font_size = 150,
                background_color = [24/255,2/255,78/255,0],
                cursor_color = [127/255,255/255,212/255,0.5],
                foreground_color = [127/255,255/255,212/255,0.5],
                input_filter = 'int',
                multiline = False,
                hint_text = "00",
                hint_text_color = [127/255,255/255,212/255,0.5],
                size_hint = [None,None],
                height = 200,
                width = 180,
            )
            self.til2.append(ti2)
            bl1.add_widget(ti2)
            #БЛОК2
            ti3 = ti_1(
                font_size = 150,
                background_color = [24/255,2/255,78/255,0],
                cursor_color = [127/255,255/255,212/255,0.5],
                foreground_color = [127/255,255/255,212/255,0.5],
                input_filter = 'int',
                multiline = False,
                hint_text = "00",
                hint_text_color = [127/255,255/255,212/255,0.5],
                size_hint = [None,None],
                height = 200,
                width = 180,
            )
            self.til3.append(ti3)
            bl2.add_widget(ti3)
            lbc2 = Label(
                text = ":",
                color = [127/255,255/255,212/255,0.5],
                font_size = 150,
                size_hint = [None,None],
                height = 230,
                width = 100,
                valign = 'top',
                halign = 'center',
            )
            bl2.add_widget(lbc2)
            ti4 = ti_2(
                font_size = 150,
                background_color = [24/255,2/255,78/255,0],
                cursor_color = [127/255,255/255,212/255,0.5],
                foreground_color = [127/255,255/255,212/255,0.5],
                input_filter = 'int',
                multiline = False,
                hint_text = "00",
                hint_text_color = [127/255,255/255,212/255,0.5],
                size_hint = [None,None],
                height = 200,
                width = 180,
            )
            self.til4.append(ti4)
            bl2.add_widget(ti4)
            #Блок с датой
            bl0.add_widget(Label(
                text = i.strftime("%d.%m.%Y"),
                font_size = 180,
                color = [127/255,255/255,212/255,1],
                size_hint = [1,None],
                height = 150,
            ))
            #Присоединение блоков в основной каркас данных 
            glv.add_widget(bl1)
            glv.add_widget(bl2)
            #Присоединение каркаса к главному экрану
            bl0.add_widget(glv)
        bl0.add_widget(bt)
        sv.add_widget(bl0)
        #Активный логотип
        self.icon = 'logo.jpg'
        pl = GeneralLayout()
        pl.add_widget(sv)
    
        return pl
    
    def save_data(self, instance):
        # Сохранение данных для первого набора TextInput
        data1 = [(ti1.text, ti2.text)
                 for ti1, ti2 in zip(self.til1, self.til2)]
        if any(data1):
            with open("saved_data1.json", "w") as file:
                json.dump(data1, file)
                print("Data for TextInput1 saved successfully to saved_data1.json")
        else:
            print("No data for TextInput1 to save")

        # Сохранение данных для второго набора TextInput
        data2 = [(ti3.text, ti4.text)
                 for ti3, ti4 in zip(self.til3, self.til3)]
        if any(data2):
            with open("saved_data2.json", "w") as file:
                json.dump(data2, file)
                print("Data for TextInput2 saved successfully to saved_data2.json")
        else:
            print("No data for TextInput2 to save")

    def on_start(self):
        # Загрузка данных для первого набора TextInput
        try:
            with open("saved_data1.json", "r") as file:
                data1 = json.load(file)
                for (ti1, ti2), saved_data in zip(zip(self.til1, self.til2), data1):
                    if saved_data:
                        ti1.text, ti2.text = saved_data
                        print("Data for TextInput1 loaded successfully")
                    else:
                        print("No data for TextInput1 found in the file")
        except FileNotFoundError:
            print("No data file for TextInput1 found")
        except json.JSONDecodeError:
            print("Error decoding JSON data for TextInput1")

        # Загрузка данных для второго набора TextInput
        try:
            with open("saved_data2.json", "r") as file:
                data2 = json.load(file)
                for (ti3, ti4), saved_data in zip(zip(self.til3, self.til4), data2):
                    if saved_data:
                        ti3.text, ti4.text = saved_data
                        print("Data for TextInput2 loaded successfully")
                    else:
                        print("No data for TextInput2 found in the file")
        except FileNotFoundError:
            print("No data file for TextInput2 found")
        except json.JSONDecodeError:
            print("Error decoding JSON data for TextInput2")
    
if __name__ == '__main__':
    SleepyLogApp().run()