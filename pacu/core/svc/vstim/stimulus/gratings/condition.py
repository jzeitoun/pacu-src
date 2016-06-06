from pacu.util.inspect import repr

class Condition(object):
    def __init__(self, ori=0, sf=0, tf=0):
        self.ori = ori
        self.sf = sf
        self.tf = tf
    __repr__ = repr.auto_strict

class RevContModCondition(object):
    def __init__(self, ori=270, sf=0):
        self.ori = ori
        self.sf = sf
    __repr__ = repr.auto_strict
