from machine import Pin

class Relay:
    def __init__(self):
        self.p = Pin(4, Pin.OUT)
    def on(self):
        self.p.on()
    def off(self):
        self.p.off()
    def get_value(self):
        return self.p.value()
    # def flash(self, n, t=500):
    #     from time import sleep_ms
    #     for i in range(n):
    #         self.on()
    #         sleep_ms(t)
    #         self.off()
    #         sleep_ms(t)
