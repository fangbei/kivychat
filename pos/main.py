import kivy
kivy.require('1.9.0')

from kivy.app import App
from kivy.core.window import Window
Window.clearcolor = (0.75, 0.75, 0.75, 1)
from kivy.uix.floatlayout import FloatLayout


class MainBox(FloatLayout):
    pass


class MainApp(App):
    def build(self):
        return MainBox()


if __name__ == '__main__':
    MainApp().run()
