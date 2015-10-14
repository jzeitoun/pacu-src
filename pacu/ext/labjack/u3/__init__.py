import time

try:
    import u3
except ImportError:
    U3 = None
else:
    U3 = u3.U3

class U3Resource(object):
    timer0 = u3.Timer0()
    timer1 = u3.Timer1()
    counter = u3.Counter0()
    def __init__(self, instance, horigin, lorigin, high, low):
        self.instance = instance
        self.horigin = horigin
        self.lorigin = lorigin
        self.high = high
        self.low = low
    def get_time(self):
        high, low = self.instance.getFeedback(self.timer1, self.timer0)
        tick = '{:b}{:032b}'.format(high-self.high, low-self.low)
        return int(tick, 2) * 2.5e-07
    def get_origin(self):
        high, low = self.instance.getFeedback(self.timer1, self.timer0)
        tick = '{:b}{:032b}'.format(high-self.horigin, low-self.lorigin)
        return int(tick, 2) * 2.5e-07
    def get_counter(self):
        return self.instance.getFeedback(self.counter)[0]

class U3Proxy(object):
    t0config = u3.Timer0Config(TimerMode=10)
    t1config = u3.Timer1Config(TimerMode=11)
    timer0 = u3.Timer0()
    timer1 = u3.Timer1()
    horigin = None
    lorigin = None
    def __init__(self):
        self.instance = U3(debug=False, autoOpen=False)
    def __enter__(self):
        self.instance.open()
        self.instance.configIO(
            TimerCounterPinOffset=4, NumberOfTimersEnabled=2,
            EnableCounter0=True, EnableCounter1=0, FIOAnalog=0)
        _, _, low, high = self.instance.getFeedback(
            self.t0config, self.t1config, self.timer0, self.timer1)
        self.horigin = self.horigin or high
        self.lorigin = self.lorigin or low
        return U3Resource(self.instance, self.horigin, self.lorigin, high, low)
    def __exit__(self, type, value, tb):
        self.instance.close()
