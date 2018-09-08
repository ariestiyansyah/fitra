import machine, time

np=machine.Neopixel(machine.Pin(13), 24)

def display_reactors(reactors, delay=20, color=220.0, brightness=0.2, clear=False):
    last_reactor = 0
    for reactor in reactors:
        np.setHSB(reactor, color, 1.0, brightness, 1, False)
        np.show()
        time.sleep_ms(delay)
        last_reactor = reactor
    if clear:
        np.clear()

display_reactors(range(1, 17))
