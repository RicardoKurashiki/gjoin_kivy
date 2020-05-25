from kivy.lang import Builder
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.properties import NumericProperty, ObjectProperty

from kivymd.app import MDApp
from kivymd.uix.snackbar import Snackbar
from kivymd.toast import toast

root_kv = """
#:import Window kivy.core.window.Window


Screen:
    name: "snackbar"

    BoxLayout:
        orientation: "vertical"
        spacing: dp(10)

        MDToolbar:
            title: "Snackbar"

        BoxLayout:
            orientation: "vertical"
            spacing: dp(10)
            padding: dp(10)

            Widget:

            MDRaisedButton:
                text: "Create simple snackbar"
                pos_hint: {"center_x": .5}
                on_release: app.show_example_snackbar("simple")

            MDRaisedButton:
                text: "Create snackbar with button"
                pos_hint: {"center_x": .5}
                on_release: app.show_example_snackbar("button")

            MDRaisedButton:
                text: "Create snackbar with a lot of text"
                pos_hint: {"center_x": .5}
                on_release: app.show_example_snackbar("verylong")

            MDSeparator:

            MDLabel:
                text: "Click the MDFloatingActionButton to show the following example..."
                halign: "center"

            Widget:

    MDFloatingActionButton:
        id: button
        md_bg_color: app.theme_cls.primary_color
        x: Window.width - self.width - dp(10)
        y: dp(10)
        on_release: app.show_example_snackbar("float")
"""


class MainApp(MDApp):
    _interval = 0
    my_snackbar = None

    def build(self):
        self.root = Builder.load_string(root_kv)

    def show_example_snackbar(self, snack_type):
        def callback(instance):
            toast(instance.text)

        def wait_interval(interval):
            self._interval += interval
            if self._interval > self.my_snackbar.duration:
                Animation(y=dp(10), d=0.2).start(self.root.ids.button)
                Clock.unschedule(wait_interval)
                self._interval = 0
                self.my_snackbar = None

        if snack_type == "simple":
            Snackbar(text="This is a snackbar!").show()
        elif snack_type == "button":
            Snackbar(
                text="This is a snackbar",
                button_text="with a button!",
                button_callback=callback,
            ).show()
        elif snack_type == "verylong":
            Snackbar(
                text="This is a very very very very very very very " "long snackbar!"
            ).show()
        elif snack_type == "float":
            if not self.my_snackbar:
                self.my_snackbar = Snackbar(
                    text="This is a snackbar!",
                    button_text="Button",
                    duration=3,
                    button_callback=callback,
                )
                self.my_snackbar.show()
                anim = Animation(y=dp(72), d=0.2)
                anim.bind(
                    on_complete=lambda *args: Clock.schedule_interval(wait_interval, 0)
                )
                anim.start(self.root.ids.button)


MainApp().run()