import speech_recognition as sr
from Interface import Interface


class InterfaceListener(Interface):
    # define static instance to keep singleton InterfaceListener object
    __instance = None

    # static method to get InterfaceListener instance
    @staticmethod
    def get_listener(lock):
        if InterfaceListener.__instance is None:
            InterfaceListener(lock)
        return InterfaceListener.__instance

    # constructor
    def __init__(self, lock):
        if InterfaceListener.__instance is not None:
            raise Exception("A Listener instance has been already created...!")
        else:
            self.lock = lock
            InterfaceListener.__instance = self

    # concrete communicate method
    def communicate(self):
        # self.lock.acquire()
        with self.lock:
            speech_recognizer = sr.Recognizer()

            with sr.Microphone() as source:
                print("Listening...")
                audio = speech_recognizer.listen(source)

            try:
                text = speech_recognizer.recognize_google(audio)
                print("you said :" + text)
                # self.lock.release()
                return text

            except sr.UnknownValueError:
                print("Your response cannot be identified")

            except sr.RequestError:
                print("Error, Check the internet connection")
            # self.lock.release()
            return False
