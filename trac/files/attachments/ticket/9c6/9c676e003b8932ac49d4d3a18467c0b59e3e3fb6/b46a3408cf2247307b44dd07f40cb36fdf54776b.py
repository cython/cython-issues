class Base(object):
    """Base class"""

    def method(self):
        return "Base"


class Derived(Base):
    """Class defived from Base"""

    def method(self):
        return "Derived"
