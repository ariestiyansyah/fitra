import sys
import logging
import connect


logging.basicConfig(logging.DEBUG)
log = logging.getLogger(__name__)


sys.path.append('/flash/src/upy')
sys.path.append('/flash/src/webthing')
sys.path.append('/flash/src/neopixel')

from webserver import run_server

connect.connect_to_ap()
connect.start_ntp()

def start_server():
	run_server()

