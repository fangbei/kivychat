import kivy
kivy.require('1.9.0')

from kivy.app import App
from kivy.uix.label import Label


class HelloLabel(Label):
    pass


class HelloApp(App):
    def build(self):
        return HelloLabel()


if __name__ == '__main__':
    HelloApp().run()
