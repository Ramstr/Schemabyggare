
class Led2:
    """ Object: Led = Leader"""
    def __init__(self, name, isHl, index):
        self.name = name
        self.isHl = isHl  # bool
        self.available = []  # list of bools
        self.total = []  # list of types ("A","B"...)
        self.hours = []  # list of int
        self.hours_tot = 0
        self.isUnderh = []  # list of bools
        self.index = index
