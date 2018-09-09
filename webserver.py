import logging
import time
import machine
from property import Property
from thing import Thing
from value import Value
from server import MultipleThings, WebThingServer
from np import start_the_reactors, blink_enemy, ultraman_mode


log = logging.getLogger(__name__)

NEOPIXEL_PIN = 13
START = 1
BLINK = 2
ULTRAMAN = 3


class Led(Thing):

	def __init__(self, ledPin):
		Thing.__init__(self,
			       'My Reactor',
			       ['OnOffSwitch', 'Light'],
			       'My Reactor built with SparkFun ESP32 Thing')
		self.np = machine.Neopixel(machine.Pin(ledPin, machine.Pin.OUT), 24)
		self.on = False
		self.action = None
		
		self.add_property(
			Property(self,
				 'start',
				 Value(self.on, self.startMyReactor),
				 metadata={
					'@type': 'OnOffProperty',
					'label': 'Start My Reactor',
					'type': 'boolean',
					'description': 'Turn on the Reactor',
				 }))
		self.add_property(
			Property(self,
				 'blink',
				 Value(self.on, self.blinkEnemy),
				 metadata={
					'@type': 'OnOffProperty',
					'label': 'Enemy Spotted',
					'type': 'boolean',
					'description': 'Enemy Spotted',
				 }))
		self.add_property(
			Property(self,
				 'ultraman',
				 Value(self.on, self.ultramanMode),
				 metadata={
					'@type': 'OnOffProperty',
					'label': 'Become Ultraman',
					'type': 'boolean',
					'description': 'Become Ultraman',
				 }))
		self.updateLed()

	def startMyReactor(self, onOff):
		self.on = onOff
		self.action = START
		self.updateLed()

	def blinkEnemy(self, onOff):
		self.on = onOff
		self.action = BLINK
		self.updateLed()

	def ultramanMode(self, onOff):
		self.on = onOff
		self.action = ULTRAMAN
		self.updateLed()

	def updateLed(self):
		log.debug('Reactor updated: ' + str(self.on))
		if self.on:
			if self.action == START:
				start_the_reactors(self.np)
			elif self.action == BLINK:
				blink_enemy(self.np)
			elif self.action == ULTRAMAN:
				ultraman_mode(self.np)
			else:
				log.info('action not found')
				self.np.clear()
		else:
			self.np.clear()


def run_server():
	log.info('run_server')

	led = Led(NEOPIXEL_PIN)
	
	server = WebThingServer(MultipleThings([led], 'SparkFun-ESP32-Thing'), port=80)

	try:
		log.info('starting the server')
		server.start()
	except KeyBoardInterrupt:
		log.info('stopping the server')
		server.stop()
		log.info('done')

