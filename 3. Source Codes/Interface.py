from abc import ABC, abstractmethod

class Interface(ABC):

    # abstract communicate method
    @abstractmethod
    def communicate(self):
        pass
