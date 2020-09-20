import os
from pynput.keyboard import Key, Listener

from  InterfaceSpeaker import InterfaceSpeaker


class KeyListener:
    # define static instance to keep singleton KeyListener object
    __instance = None

    # static method to get KeyListener instance
    @staticmethod
    def get_key_listener(main):
        if KeyListener.__instance is None:
            KeyListener(main)
        return KeyListener.__instance

    # constructor
    def __init__(self,main):
        if KeyListener.__instance is not None:
            raise Exception("A Key Listener instance has been already created...!")
        else:
            self.main = main
            self.pressed_once = False
            self.listener = None
            KeyListener.__instance = self

    # catch key press event
    def listen_for_key(self):
        with Listener(on_press=self.check_key) as self.listener:
            self.listener.join()

    # process key press event
    def check_key(self, key):
        if key == Key.esc:
            # if isinstance(self.main.user_interface, InterfaceSpeaker):
            #     self.main.user_interface.quit()
            if not self.pressed_once:
                self.pressed_once = True
                self.main.instruct('confirm_termination')
                self.listen_for_key()
            else:
                self.main.quit()
        else:
            self.pressed_once = False
