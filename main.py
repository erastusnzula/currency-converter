from datetime import datetime

import requests
from kivy.app import App
from kivy.metrics import dp
from kivy.properties import NumericProperty, StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput


class CurrencyConverterWidget(BoxLayout):
    amount_text = None
    current_date = datetime.now().strftime('%d - %m - %Y')
    from_c = StringProperty("KES")
    to_c = StringProperty("USD")
    amount_to_convert = NumericProperty(115.66)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.url = 'https://api.exchangerate-api.com/v4/latest/USD'
        self.data = requests.get(self.url).json()
        self.currencies = self.data['rates']

        self.from_dropdown = DropDown()
        self.to_dropdown = DropDown()
        for c in self.currencies.keys():
            btn = Button(text=str(c), background_color=(0.4, .4, .4), background_normal='', size_hint_y=None, height=44,
                         on_release=lambda btn_from: self.from_dropdown.select(btn_from.text))
            btn_to = Button(text=str(c), background_color=(0, .6, .4), background_normal='', size_hint_y=None,
                            height=44,
                            on_release=lambda btn_to_f: self.to_dropdown.select(btn_to_f.text))
            self.from_dropdown.add_widget(btn)
            self.to_dropdown.add_widget(btn_to)
        self.main_from_button = Button(text=self.from_c, size_hint=(1, 1),
                                       on_release=self.open_from_dropdown, background_down='assets/images/btn.png',
                                       background_normal='assets/images/btn.png',
                                       font_name='assets/fonts/Eurostile.ttf',
                                       font_size=dp(25))
        self.main_to_button = Button(text=self.to_c, size_hint=(1, 1),
                                     on_release=self.open_to_dropdown, background_down='assets/images/back.png',
                                     background_normal='assets/images/back.png', font_name='assets/fonts/Eurostile.ttf',
                                     font_size=dp(25))
        self.from_dropdown.bind(on_select=self.get_from_selected)
        self.to_dropdown.bind(on_select=self.get_to_selected)

        self.box = BoxLayout()
        self.box.add_widget(self.main_from_button)
        self.box.add_widget(Label(size_hint=(1, 1)))
        self.box.add_widget(self.main_to_button)
        self.add_widget(self.box)
        self.add_widget(Label())
        self.box_1 = BoxLayout()
        self.amount_text = TextInput(hint_text="Amount", text=str(self.amount_to_convert),
                                     font_name='assets/fonts/AovelSansRounded-rdDL.ttf', font_size=dp(25),
                                     size_hint=(.7, 1),
                                     cursor_color=(0, 0, 0), background_active='', background_normal='')
        self.box_1.add_widget(self.amount_text)
        self.output = Label(font_name='assets/fonts/AovelSansRounded-rdDL.ttf', font_size=dp(25), color=(0, 0, 0))
        self.box_1.add_widget(self.output)
        self.add_widget(self.box_1)
        self.output_label = Label(font_name='assets/fonts/AovelSansRounded-rdDL.ttf', color=(0, 0, 0), font_size=dp(20))
        self.add_widget(Label())
        self.add_widget(
            Button(text="CONVERT", on_release=self.convert, background_down='assets/images/btn.png',
                   background_normal='assets/images/btn.png',
                   font_name='assets/fonts/ShortBaby-Mg2w.ttf', size_hint=(.9, 1), pos_hint={'center_x': .5}))
        self.add_widget(self.output_label)

    def open_from_dropdown(self, *args):
        self.from_dropdown.open(*args)

    def get_from_selected(self, instance, text):
        self.main_from_button.text = text
        self.from_c = text

    def open_to_dropdown(self, *args):
        self.to_dropdown.open(*args)

    def get_to_selected(self, instance, text):
        self.main_to_button.text = text
        self.to_c = text

    def convert(self, *args):
        from_ = self.from_c
        to = self.to_c
        amount = float(self.amount_text.text)
        if from_ != 'USD':
            amount = amount / self.currencies[from_]
        amount = round(amount * self.currencies[to], 4)
        self.output.text = str(amount)
        self.output_label.text = f"{self.amount_text.text} {self.from_c} = {str(amount)} {self.to_c}"
        print(amount)
        return amount


class ConverterApp(App):
    def build(self):
        return CurrencyConverterWidget()


ConverterApp().run()
