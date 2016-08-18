cdef class Spam:
    cdef dict d

    def __init__(self):
        self.d = {"A": "a", "B": "b", "C": "c"}

    def spam(self, Spam other):
        if len(self.d) != len(other.d):
            return False

        for elm in self.d.iterkeys():
            if elm not in other.d:
                # A decref for the return value in the above 'return False'
                # statement is generated, even though the statement was
                # never executed.
                return False

        return True

    # Codegen for this looks fine.
    def spork(self, Spam other):
        if len(self.d) != len(other.d):
            return False

        if len(self.d) == len(other.d):
            return False

        return True


a = Spam()
b = Spam()
a.spam(b)
