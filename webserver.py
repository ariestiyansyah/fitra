import logging
import time
import machine
from property import Property
from thing import Thing
from value import Value
from server import MultipleThings, WebThingServer
from np import start_the_reactors, blink_enemy, ultraman_mode, rotate, display_odd


log = logging.getLogger(__name__)

NEOPIXEL_PIN = 13
START = 1
BLINK = 2
ULTRAMAN = 3
SPIN = 4
ODD = 5


class Led(Thing):

	def __init__(self, ledPin):
		Thing.__init__(self,
			       'My Reactor',
			       ['OnOffSwitch', 'Light'],
			       'My Reactor built with SparkFun ESP32 Thing')
		self.ledPin = ledPin
		self.np = machine.Neopixel(machine.Pin(ledPin, machine.Pin.OUT), 24)
		self.brightness = 20
		self.blue = 0
		self.color = '#0055FF'
		self.green = 0
		self.red = 0
		self.on = False
		self.start = False
		self.odd = False
		self.action = None

		self.add_property(
			Property(self,
				 'on',
				 Value(self.on, self.spinningReactor),
				 metadata={
					'@type': 'OnOffProperty',
					'label': 'Spinning Reactor',
					'type': 'boolean',
					'description': 'Turn on the Reactor',
				 }))
		self.add_property(
			Property(self,
				 'start',
				 Value(self.start, self.bootReactor),
				 metadata={
					'@type': 'OnOffProperty',
					'label': 'Start My Reactor',
					'type': 'boolean',
					'description': 'Turn on the Reactor',
				 }))
		self.add_property(
			Property(self,
				 'odd',
				 Value(self.odd, self.oddReactor),
				 metadata={
					'@type': 'OnOffProperty',
					'label': 'Display Odd Reactor',
					'type': 'boolean',
					'description': 'Turn on the Reactor',
				 }))
		self.add_property(
			Property(self,
				 'brightness',
				 Value(self.brightness, self.ultramanMode),
				 metadata={
					'@type': 'BrightnessProperty',
					'label': 'Become Ultraman',
					'type': 'number',
					'description': 'Become Ultraman',
					'min': 0,
					'max': 100,
					'unit': 'percent',
				 }))
		self.add_property(
			Property(self,
				 'color',
				 Value(self.color, self.blinkEnemy),
				 metadata={
					'@type': 'ColorProperty',
					'label': 'Blink Enemy',
					'type': 'string',
					'description': 'Blink Enemy',
				 }))
		self.updateReactor()

	def constructNp(self):
		self.np = machine.Neopixel(machine.Pin(self.ledPin, machine.Pin.OUT), 24)

	def spinningReactor(self, onOff):
		self.on = onOff
		self.action = SPIN
		self.updateReactor()

	def bootReactor(self, onOff):
		self.start = onOff
		self.action = START
		self.updateReactor()

	def oddReactor(self, onOff):
		self.odd = onOff
		self.action = ODD
		self.updateReactor()

	def convertToRgb(self, color):
		red = int(color[1:3], 16) / 256 * 100
		green = int(color[3:5], 16) / 256 * 100
		blue = int(color[5:7], 16) / 256 * 100
		return (red, green, blue)

	def convertToHex(self, color):
		return int(hex(int(color[1:], 16)), 16)

	def blinkEnemy(self, color):
		self.color = color
		self.red, self.green, self.blue = self.convertToRgb(color)
		self.action = BLINK
		self.updateReactor()

	def ultramanMode(self, brightness):
		self.brightness = brightness
		self.action = ULTRAMAN
		self.updateReactor()

	def updateReactor(self):
		if not self.on and not self.start and not self.odd:
			#self.np.deinit()
			#self.constructNp()
			self.np.clear()
			return

		#log.debug("Reactor Updated, action: {}".format(self.action))
		#log.debug("brightness: {}".format(self.brightness))
		#log.debug("on: {}".format(self.on))
		#log.debug("red: {}, green: {}, blue: {}".format(self.red, self.green, self.blue))
		hex_color = self.convertToHex(self.color)
		#log.debug("hex: {}".format(hex_color))
		hue, saturation, brightness = self.np.RGBtoHSB(hex_color)

		if self.action == SPIN:
			log.debug("rotate")
			rotate(self.np, 20, hue, saturation, brightness)
		elif self.action == START:
			log.debug("start")
			start_the_reactors(self.np, 250, hue, saturation, brightness, False)
		elif self.action == ODD:
			log.debug("display odd")
			display_odd(self.np, 250, hue, saturation, brightness, False)


def run_server():
	log.info('run_server')

	led = Led(NEOPIXEL_PIN)
	start_the_reactors(led.np, 250, clear=True)

	server = WebThingServer(MultipleThings([led], 'SparkFun-ESP32-Thing'), port=80)

	try:
		log.info('starting the server')
		server.start()
	except KeyBoardInterrupt:
		log.info('stopping the server')
		server.stop()
		log.info('done')

