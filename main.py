from kivy.app import App
from kivymd.app import MDApp
from kivy.core.window import Window

from libs.uix.root import Root


class MainApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.title = "Kivy - Lazy Load"

        Window.keyboard_anim_args = {"d": 0.2, "t": "linear"}
        Window.softinput_mode = "below_target"
        Window.size = (1080,2220)

    def build(self):
        # Don't change self.root to self.some_other_name
        # refer https://kivy.org/doc/stable/api-kivy.app.html#kivy.app.App.root
        self.root = Root()
        self.root.set_current("home")


if __name__ == "__main__":
    MainApp().run()
