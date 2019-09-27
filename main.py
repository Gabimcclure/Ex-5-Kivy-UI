import os
import pygame

from kivy.app import App
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import StringProperty
from kivy.animation import Animation
from kivy.uix.slider import Slider

from pidev.MixPanel import MixPanel
from pidev.kivy.PassCodeScreen import PassCodeScreen
from pidev.kivy.PauseScreen import PauseScreen
from pidev.kivy import DPEAButton
from pidev.kivy import ImageButton
from pidev.Joystick import Joystick

from threading import Thread
from time import sleep

MIXPANEL_TOKEN = "x"
MIXPANEL = MixPanel("Project Name", MIXPANEL_TOKEN)

SCREEN_MANAGER = ScreenManager()
MAIN_SCREEN_NAME = 'main'
ADMIN_SCREEN_NAME = 'admin'
IMAGE_SCREEN_NAME = 'image'


class ProjectNameGUI(App):
    """
    Class to handle running the GUI Application
    """

    def build(self):
        """
        Build the application
        :return: Kivy Screen Manager instance
        """
        return SCREEN_MANAGER


Window.clearcolor = (1, 1, 1, 1)  # White

class MainScreen(Screen):


    """
    Class to handle the main screen and its associated touch events
    """

    string_value = StringProperty()

    def __init__(self, **kwargs):
        super(MainScreen,self).__init__(**kwargs)
        self.count = 0


    def pressed(self):
        """
        Function called on button touch event for button with id: testButton
        :return: None
        """
        PauseScreen.pause(pause_scene_name='pauseScene', transition_back_scene='main', text="Test", pause_duration=5)


    def pressed2(self):
        self.count = self.count + 1
        self.string_value = str(self.count)

    def admin_action(self):
        """
        Hidden admin button touch event. Transitions to passCodeScreen.
        This method is called from pidev/kivy/PassCodeScreen.kv
        :return: None
        """
        SCREEN_MANAGER.current = 'passCode'

    def image_screen(self):

        SCREEN_MANAGER.current = 'image'

    def joy_update(self):
        while True:
            self.joy_x_val = joystick.get_axis('x')
            self.joy_y_val = joystick.get_axis('y')
            # your code to update the labels here
            sleep(.1)

    def start_joy_thread(self):
        Thread(target=self.joy_update).start()

class AdminScreen(Screen):
    """
    Class to handle the AdminScreen and its functionality
    """

    def __init__(self, **kwargs):
        """
        Load the AdminScreen.kv file. Set the necessary names of the screens for the PassCodeScreen to transition to.
        Lastly super Screen's __init__
        :param kwargs: Normal kivy.uix.screenmanager.Screen attributes
        """
        Builder.load_file('AdminScreen.kv')

        PassCodeScreen.set_admin_events_screen(ADMIN_SCREEN_NAME)  # Specify screen name to transition to after correct password
        PassCodeScreen.set_transition_back_screen(MAIN_SCREEN_NAME)  # set screen name to transition to if "Back to Game is pressed"

        super(AdminScreen, self).__init__(**kwargs)

class ImageScreen(Screen):

    joystick = Joystick(0, False)

    def __init__(self, **kwargs):

        Builder.load_file('ImageScreen.kv')

        super(ImageScreen, self).__init__(**kwargs)

    def animation(self):
        self.anim = Animation(x=50) + Animation(size=(80, 80), duration=2.)
        self.anim += Animation(x= 75) + Animation(size=(100,40), duration= 1.5)
        self.anim += Animation(x=150) + Animation(size=(500, 340), duration=1.5)
        self.anim += Animation(x=300) + Animation(size=(100, 40), duration=1.5)
        self.anim.repeat = True
        self.anim.start(self.ids.animation)

    def joybuttons(self):
        for x in range(11):
            if self.joystick.get_button_state(x)==1:
                self.ids.jbuttons.text = "Button Pressed: " + str(x)

    @staticmethod
    def transition_back():
        """
        Transition back to the main screen
        :return:
        """
        SCREEN_MANAGER.current = MAIN_SCREEN_NAME

    @staticmethod
    def shutdown():
        """
        Shutdown the system. This should free all steppers and do any cleanup necessary
        :return: None
        """
        os.system("sudo shutdown now")

    @staticmethod
    def exit_program():
        """
        Quit the program. This should free all steppers and do any cleanup necessary
        :return: None
        """
        quit()
"""
Widget additions
"""

Builder.load_file('main.kv')
SCREEN_MANAGER.add_widget(MainScreen(name=MAIN_SCREEN_NAME))
SCREEN_MANAGER.add_widget(PassCodeScreen(name='passCode'))
SCREEN_MANAGER.add_widget(PauseScreen(name='pauseScene'))
SCREEN_MANAGER.add_widget(AdminScreen(name=ADMIN_SCREEN_NAME))
SCREEN_MANAGER.add_widget(ImageScreen(name=IMAGE_SCREEN_NAME))

"""
MixPanel
"""


def send_event(event_name):
    """
    Send an event to MixPanel without properties
    :param event_name: Name of the event
    :return: None
    """
    global MIXPANEL

    MIXPANEL.set_event_name(event_name)
    MIXPANEL.send_event()


if __name__ == "__main__":
    # send_event("Project Initialized")
    # Window.fullscreen = 'auto'
    ProjectNameGUI().run()
