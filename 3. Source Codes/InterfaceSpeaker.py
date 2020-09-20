from gtts import gTTS
from pygame import mixer
import os

from Interface import Interface
import threading

dirname = os.path.dirname(__file__)


class InterfaceSpeaker(Interface):
    # define static instance to keep singleton InterfaceSpeaker object
    __instance = None

    # static method to get InterfaceSpeaker instance
    @staticmethod
    def get_speaker(lock):
        if InterfaceSpeaker.__instance is None:
            InterfaceSpeaker(lock)
        return InterfaceSpeaker.__instance

    # constructor
    def __init__(self, lock):
        if InterfaceSpeaker.__instance is not None:
            raise Exception("A Speaker instance has been already created...!")
        else:
            self.lock = lock
            InterfaceSpeaker.__instance = self

    # synchronization method
    def synchronized(func):

        func.__lock__ = threading.Lock()

        def synced_func(*args, **kws):
            with func.__lock__:
                return func(*args, **kws)

        return synced_func

    # concrete communicate method
    @synchronized
    def communicate(self, text_input, file_name, temp):
        with self.lock:
            file_path = os.path.join(dirname, 'audio_samples/' + file_name + ".mp3")
            if not os.path.isfile(file_path):
                try:
                    text_to_speech_read = gTTS(text=text_input, lang='en')
                    text_to_speech_read.save(file_path)
                except:
                    os.remove(file_path)
                    file_path = os.path.join(dirname, "audio_samples/no_internet.mp3")

            mixer.init()
            mixer.music.load(file_path)
            mixer.music.play()

            while mixer.music.get_busy():
                continue

            mixer.music.load(os.path.join(dirname, 'audio_samples/bogus.mp3'))
            mixer.quit()

            if temp:
                os.remove(file_path)
        # self.lock.release()

    # quit interface
    def quit(self):
        if mixer.get_init():
            mixer.music.load(os.path.join(dirname, 'audio_samples/bogus.mp3'))

