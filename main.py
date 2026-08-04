"""
CBT Registration Checker
A simple app where each student checks their own registration status
on the UNI UYO CBT portal and can share it with their class rep.
"""

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
from kivy.utils import get_color_from_hex
from kivy.clock import Clock
from kivy.metrics import dp
import os
import datetime

try:
    from android.permissions import request_permissions, Permission
    ANDROID = True
except ImportError:
    ANDROID = False

# Colors
BG     = get_color_from_hex("#0D0D0D")
CARD   = get_color_from_hex("#1A1A2E")
ACCENT = get_color_from_hex("#7C3AED")
ACCENT2= get_color_from_hex("#A855F7")
SUCCESS= get_color_from_hex("#22C55E")
WARN   = get_color_from_hex("#F59E0B")
ERROR  = get_color_from_hex("#EF4444")
WHITE  = get_color_from_hex("#F1F5F9")
GREY   = get_color_from_hex("#94A3B8")

# NOTE: Do NOT set Window.clearcolor at module level — causes crash on Android
# It's set in on_start() instead

PORTAL_URL = "https://cbt.uniuyo.edu.ng/auth"


class CheckScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)

        scroll = ScrollView(size_hint=(1, 1))
        root = BoxLayout(orientation="vertical", padding=dp(24), spacing=dp(16),
                         size_hint_y=None)
        root.bind(minimum_height=root.setter("height"))
        scroll.add_widget(root)

        # Title
        root.add_widget(Label(
            text="CBT Registration Checker",
            font_size=dp(22), bold=True, color=ACCENT2,
            size_hint_y=None, height=dp(50),
            halign="center", valign="middle"
        ))
        root.add_widget(Label(
            text="Check YOUR registration status only.",
            font_size=dp(12), color=GREY,
            size_hint_y=None, height=dp(30),
            halign="center"
        ))
        root.add_widget(Label(
            text="Enter your own registration number below.",
            font_size=dp(11), color=GREY,
            size_hint_y=None, height=dp(25),
            halign="center"
        ))

        root.add_widget(BoxLayout(size_hint_y=None, height=dp(20)))

        # Reg number input
        root.add_widget(Label(
            text="Your Registration Number",
            font_size=dp(14), color=WHITE, bold=True,
            size_hint_y=None, height=dp(30),
            halign="left"
        ))
        self.reg_input = TextInput(
            hint_text="e.g. 25/CS/MB/001",
            font_size=dp(16),
            size_hint_y=None, height=dp(52),
            background_color=CARD, foreground_color=WHITE,
            hint_text_color=GREY, multiline=False,
            padding=[dp(12), dp(14), dp(12), dp(14)]
        )
        root.add_widget(self.reg_input)

        root.add_widget(BoxLayout(size_hint_y=None, height=dp(16)))

        # Check button
        self.check_btn = Button(
            text="Check My Registration",
            size_hint_y=None, height=dp(52),
            background_normal="", background_color=ACCENT,
            color=WHITE, font_size=dp(16), bold=True
        )
        self.check_btn.bind(on_release=self.do_check)
        root.add_widget(self.check_btn)

        root.add_widget(BoxLayout(size_hint_y=None, height=dp(12)))

        # Status label
        self.status_label = Label(
            text="",
            font_size=dp(13), color=GREY,
            size_hint_y=None, height=dp(80),
            halign="center", valign="top"
        )
        self.status_label.bind(size=lambda i, v: setattr(i, "text_size", v))
        root.add_widget(self.status_label)

        root.add_widget(BoxLayout(size_hint_y=None, height=dp(12)))

        # Share button (hidden until checked)
        self.share_btn = Button(
            text="Share My Status with Class Rep",
            size_hint_y=None, height=dp(48),
            background_normal="", background_color=SUCCESS,
            color=WHITE, font_size=dp(14), bold=True,
            disabled=True, opacity=0
        )
        self.share_btn.bind(on_release=self.do_share)
        root.add_widget(self.share_btn)

        root.add_widget(BoxLayout(size_hint_y=None, height=dp(24)))

        # Info section
        root.add_widget(Label(
            text="How this works",
            font_size=dp(15), color=ACCENT2, bold=True,
            size_hint_y=None, height=dp(35),
            halign="left"
        ))
        info = (
            "1. Enter YOUR registration number only.\n"
            "2. Tap Check - the app opens the CBT portal.\n"
            "3. Complete the check in the browser (tick the box, submit).\n"
            "4. Come back to the app and tap Share to report to your class rep.\n\n"
            "This app checks one number at a time - yours.\n"
            "Do not use it to check other students numbers without consent."
        )
        info_label = Label(
            text=info,
            font_size=dp(12), color=GREY,
            size_hint_y=None, height=dp(180),
            halign="left", valign="top"
        )
        info_label.bind(size=lambda i, v: setattr(i, "text_size", v))
        root.add_widget(info_label)

        self.reg_number = ""
        self.add_widget(scroll)

    def do_check(self, *_):
        reg = self.reg_input.text.strip()
        if not reg:
            self.status_label.text = "Please enter your registration number."
            self.status_label.color = WARN
            return

        self.reg_number = reg

        if ANDROID:
            try:
                from jnius import autoclass
                Intent = autoclass("android.content.Intent")
                Uri = autoclass("android.net.Uri")
                PythonActivity = autoclass("org.kivy.android.PythonActivity")

                intent = Intent(Intent.ACTION_VIEW)
                intent.setData(Uri.parse(PORTAL_URL))
                PythonActivity.mActivity.startActivity(intent)

                self.status_label.text = (
                    "Browser opened. Complete your check there,\n"
                    "then come back and tap Share to report."
                )
                self.status_label.color = SUCCESS
                self.share_btn.disabled = False
                self.share_btn.opacity = 1
            except Exception as e:
                self.status_label.text = "Error: " + str(e)[:80]
                self.status_label.color = ERROR
        else:
            import webbrowser
            webbrowser.open(PORTAL_URL)
            self.status_label.text = "Browser opened. Complete your check there."
            self.status_label.color = SUCCESS
            self.share_btn.disabled = False
            self.share_btn.opacity = 1

    def do_share(self, *_):
        if not self.reg_number:
            return

        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        share_text = (
            "CBT Registration Status Report\n"
            "Reg No: %s\n"
            "Status: Checked on %s\n"
            "(Please verify in the portal yourself)\n"
            "- Sent via CBT Registration Checker"
        ) % (self.reg_number, now)

        if ANDROID:
            try:
                from jnius import autoclass
                Intent = autoclass("android.content.Intent")
                PythonActivity = autoclass("org.kivy.android.PythonActivity")

                intent = Intent(Intent.ACTION_SEND)
                intent.setType("text/plain")
                intent.putExtra(Intent.EXTRA_TEXT, share_text)
                intent.putExtra(Intent.EXTRA_SUBJECT, "CBT Registration Status")

                chooser = Intent.createChooser(intent, "Share your status")
                PythonActivity.mActivity.startActivity(chooser)
            except Exception as e:
                self.status_label.text = "Share error: " + str(e)[:80]
                self.status_label.color = ERROR
        else:
            print(share_text)
            self.status_label.text = "Status ready to share!"
            self.status_label.color = SUCCESS


class CBTCheckerApp(App):
    def build(self):
        sm = ScreenManager(transition=SlideTransition())
        sm.add_widget(CheckScreen(name="check"))
        return sm

    def on_start(self):
        # Set background color here — safe because window is ready
        Window.clearcolor = BG

        if ANDROID:
            request_permissions([
                Permission.INTERNET,
            ])


if __name__ == "__main__":
    CBTCheckerApp().run()
