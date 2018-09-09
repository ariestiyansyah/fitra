import logging
import time


log = logging.getLogger(__name__)


REACTORS = range(1, 17)
DELAY = 20
COLOR = 220.0
BRIGHTNESS = 0.2
SATURATION = 1.0


def start_the_reactors(np, delay=DELAY, color=COLOR, saturation=SATURATION, brightness=BRIGHTNESS, clear=True):
	for reactor in REACTORS:
		np.setHSB(reactor, color, saturation, brightness, 1, False)
		np.show()
		time.sleep_ms(delay)
	if clear:
		np.clear()


def blink_enemy(np, delay=500, color=COLOR, end=7):
	for i in range(0, end):
		for reactor in REACTORS:
			np.setHSB(reactor, color, SATURATION, BRIGHTNESS, 1, False)
		np.show()
		time.sleep_ms(delay)
	np.clear()


def ultraman_mode(np, delay=250, color=0.0, end=7):
	blink_enemy(np, delay=delay, color=color, end=end)

def rotate(np, delay=DELAY, color=COLOR, saturation=SATURATION, brightness=BRIGHTNESS, end=10):
	for i in range(0, end):
		for reactor in REACTORS:
			log.debug('Set: {} to color: {}'.format(reactor, color))
			np.setHSB(reactor, color, saturation, brightness, 1, False)
			np.show()
			time.sleep_ms(delay)
			np.clear()


def display_odd(np, delay=DELAY, color=COLOR, saturation=SATURATION, brightness=BRIGHTNESS, clear=True):
	for reactor in REACTORS:
		if reactor % 2 == 1:
			continue
		np.setHSB(reactor, color, saturation, brightness, 1, False)
		np.show()
		time.sleep_ms(delay)
	if clear:
		np.clear()
