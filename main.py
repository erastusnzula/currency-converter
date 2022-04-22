import sys
from datetime import datetime

import requests
from kivy.app import App
from kivy.metrics import dp
from kivy.properties import NumericProperty, StringProperty, Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.uix.label import Label
from kivy.uix.modalview import ModalView
from kivy.uix.textinput import TextInput


class CurrencyConverterWidget(BoxLayout):
    amount_textfield = None
    current_date = datetime.now().strftime('%d - %m - %Y')
    currency_from = StringProperty("USD")
    currency_to = StringProperty("KES")
    amount_to_convert = NumericProperty(1)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        try:
            self.url = 'https://api.exchangerate-api.com/v4/latest/USD'
            self.data = requests.get(self.url).json()
            self.currencies = self.data['rates']

            self.from_dropdown = DropDown()
            self.to_dropdown = DropDown()
            for c in self.currencies.keys():
                btn = Button(text=str(c), background_color=(0.4, .4, .4), background_normal='', size_hint_y=None,
                             height=44,
                             on_release=lambda btn_from: self.from_dropdown.select(btn_from.text))
                btn_to = Button(text=str(c), background_color=(0, .6, .4), background_normal='', size_hint_y=None,
                                height=44,
                                on_release=lambda btn_to_f: self.to_dropdown.select(btn_to_f.text))
                self.from_dropdown.add_widget(btn)
                self.to_dropdown.add_widget(btn_to)
            self.main_from_button = Button(text=self.currency_from, size_hint=(1, 1),
                                           on_release=self.open_from_dropdown, background_down='assets/images/btn.png',
                                           background_normal='assets/images/btn.png',
                                           font_name='assets/fonts/Eurostile.ttf',
                                           font_size=dp(25))
            self.main_to_button = Button(text=self.currency_to, size_hint=(1, 1),
                                         on_release=self.open_to_dropdown, background_down='assets/images/back.png',
                                         background_normal='assets/images/back.png',
                                         font_name='assets/fonts/Eurostile.ttf',
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
            self.amount_textfield = TextInput(hint_text="Amount", text=str(self.amount_to_convert),
                                              font_name='assets/fonts/AovelSansRounded-rdDL.ttf', font_size=dp(25),
                                              size_hint=(.7, 1),
                                              cursor_color=(0, 0, 0), background_active='', background_normal='')
            self.box_1.add_widget(self.amount_textfield)
            self.output = Label(font_name='assets/fonts/AovelSansRounded-rdDL.ttf', font_size=dp(25), color=(0, 0, 0))
            self.box_1.add_widget(self.output)
            self.add_widget(self.box_1)
            self.output_label = Label(font_name='assets/fonts/AovelSansRounded-rdDL.ttf', color=(0, 0, 0),
                                      font_size=dp(20))
            self.add_widget(Label())
            self.add_widget(
                Button(text="CONVERT", on_release=self.convert, background_down='assets/images/btn.png',
                       background_normal='assets/images/btn.png',
                       font_name='assets/fonts/ShortBaby-Mg2w.ttf', size_hint=(.9, 1), pos_hint={'center_x': .5}))
            self.add_widget(self.output_label)
        except requests.exceptions.ConnectionError:
            self.add_widget(
                Label(text='No internet, exiting ...', font_name='assets/fonts/Eurostile.ttf',
                      font_size=dp(25), color=(1, 0, 0)))
            Clock.schedule_once(self.exit_protocol, 8)

    @staticmethod
    def exit_protocol(dt):
        sys.exit()

    def open_from_dropdown(self, *args):
        self.from_dropdown.open(*args)

    def get_from_selected(self, instance, text):
        self.main_from_button.text = text
        self.currency_from = text

    def open_to_dropdown(self, *args):
        self.to_dropdown.open(*args)

    def get_to_selected(self, instance, text):
        self.main_to_button.text = text
        self.currency_to = text

    def convert(self, *args):
        try:
            from_ = self.currency_from
            to = self.currency_to
            get_text = self.amount_textfield.text.replace(',', '')
            amount = float(get_text)
            if from_ != 'USD':
                amount = amount / self.currencies[from_]
            amount = round(amount * self.currencies[to], 4)
            self.output.text = str(f'{amount:,.2f}')
            self.output_label.text = f"{str(f'{float(get_text):,.2f}')} {self.currency_from} = {str(f'{amount:,.2f}')} {self.currency_to}"
            return amount
        except ValueError:
            self.output.text = 'Invalid input'
            self.output_label.text = 'Invalid input'


class ConverterApp(App):
    def build(self):
        self.title = 'Currency Converter'
        self.icon = 'assets/images/icon.png'
        return CurrencyConverterWidget()


ConverterApp().run()
