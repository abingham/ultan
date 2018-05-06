from abc import ABC, abstractmethod


class Strategy(ABC):
    @abstractmethod
    def get_names(self):
        """Return an iterable of `(name, module-name)` tuples. """
        pass
