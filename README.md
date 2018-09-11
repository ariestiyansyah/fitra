# Fitra - Arc Reactor using ESP32 and Web of Things

<img width="800" alt="screen shot 2018-09-10 at 02 44 46" src="https://user-images.githubusercontent.com/2667489/45268263-8b079900-b4a3-11e8-9c0f-07cea7d30864.png">

## Requirements

Requirement tools:
- SparkFun ESP32 Thing
- Jumper Male-Male 20cm
- Battery Lipo 3.7v 1000mAh
- Rainbow LED WS2812
- Solder
- Solder Iron

## HOW TO

### Datasheet and Soldering

The following datasheet is advised by my friend from SurabayaPy [Tegar Imansyah](https://github.com/tegarimansyah)

![photo6096182430420543507](https://user-images.githubusercontent.com/2667489/45268071-c903bd80-b4a1-11e8-8efd-3f3320a72e40.jpg)

Connect SparkFun and Rainbow LED WS2812 with jumper by using the following
schema

| SparkFun | Jumper     | LED WS2812 |
|----------|------------|------------|
| 13       | Connect to | DIN        |
| VBAT/VUSB| Connect to | VCC        |
| GND      | Connect to | GND        |

Use VBAT for battery power and VUSB for USB power

### Flashing Loboris Micropython

Clone the fork of Loboris Micropython repository, this repository has been
updated to allow PUT command to work with microWebSrv and fix for microWebSocket
based on [this](https://github.com/dhylands/MicroPython_ESP32_psRAM_LoBo) branch and latest update from [Loboris](https://github.com/dhylands/MicroPython_ESP32_psRAM_LoBo) master branch

```
$ git clone https://github.com/ariestiyansyah/MicroPython_ESP32_psRAM_LoBo.git
```

Config the micropython and build the Firmware
```
$ cd MicroPython_ESP32_psRAM_LoBo/MicroPython_BUILD/
$ ./BUILD.sh menuconfig
$ ./BUILD.sh
```
Flash it
```
$ ./BUILD.sh --port /dev/tty.usbserial-DN03F9EP flash
```
SparkFun connected my mac using `/dev/tty.usbserial-DN03F9EP` port, this will be
different on each device, check it using following command

```
$ ls /dev/tty.usbserial*
```

### Install Gateway

Follow instruction from
[https://github.com/mozilla-iot/gateway/blob/master/README.md](https://github.com/mozilla-iot/gateway/blob/master/README.md)
to install Mozilla Gateway in your Raspberry Pi or PC/Mac.

### Web of Things Micropython

Clone fitra project
```
$ git clone https://github.com/ariestiyansyah/fitra.git
```

Hierarchy of fitra project

```
.
├── README.md
├── config.py
├── connect.py
├── main.py
├── src
│   ├── neopixel
│   │   ├── np.py
│   ├── upy
│   │   ├── README.md
│   │   ├── copy.py
│   │   ├── eventemitter.py
│   │   ├── logging.py
│   │   ├── types.py
│   │   └── uuid.py
│   └── webthing
│       ├── action.py
│       ├── event.py
│       ├── property.py
│       ├── server.py
│       ├── thing.py
│       ├── utils.py
│       └── value.py
├── start.py
└── webserver.py
```

Rename file `config.example.py` to `config.py`, change variable SSID and PASSWORD value with wifi credentials, for example
```
SSID = 'FITRA'
PASSWORD = 'bahagialah'
```

Sync local files to ESP32 by using [rshell](https://github.com/dhylands/rshell),
you can also use ampy :) mine is rhsell.

```
$ rshell -a --buffer-size=30 -p /dev/tty.usbserial-DN03F9EP
fitra> rsync -v . /flash
fitra> repl
>>> Control-D # Soft reset
```

You will see spining LED in neopixel now.

### Adding RGB function and Property

Create sample display_odd function to display LED in odd number by

```
# src/neopixel/np.py
def display_odd(np, delay=DELAY, color=COLOR, saturation=SATURATION, brightness=BRIGHTNESS, clear=True):
    for reactor in REACTORS:
        if reactor % 2 == 1:
            continue
        np.setHSB(reactor, color, saturation, brightness, 1, False)
        np.show()
        time.sleep_ms(delay)
    if clear:
        np.clear()
```

Add property to enable it in gateway
```
# webserver.py
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
```

### Convert RGB to Hex

This function contributed by my partner in crime [Ady Rahmat MA](https://github.com/ngurajeka)
```
# webserver.py
def convertToRgb(self, color):
    red = int(color[1:3], 16) / 256 * 100
	green = int(color[3:5], 16) / 256 * 100
	blue = int(color[5:7], 16) / 256 * 100
	return (red, green, blue)

def convertToHex(self, color):
    return int(hex(int(color[1:], 16)), 16)
    hex_color = self.convertToHex(self.color)
    hue, saturation, brightness = self.np.RGBtoHSB(hex_color)
```

## Lesson Learned

all problems found during the experiment.

### LED on USB power vs Battery power

The led does not run normally when connected with USB Power, it will run
smoothly on battery power.

### Could not enter raw repl

```
rshell -a --buffer-size=30 -p /dev/tty.usbserial-DN03F9EP                              [19:09:48]
Connecting to /dev/tty.usbserial-DN03F9EP ...
b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x9as' [size: 2555904; Flash address: 0x190000]\r\n----------------\r\nFilesystem size: 2341888 B\r\n           Used: 142080 B\r\n           Free: 2199808 B\r\n----------------\r\n"
Traceback (most recent call last):
  File "/usr/local/lib/python3.7/site-packages/rshell/main.py", line 1186, in connect
    ip_address = socket.gethostbyname(port)
socket.gaierror: [Errno 8] nodename nor servname provided, or not known

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/usr/local/bin/rshell", line 11, in <module>
    load_entry_point('rshell==0.0.14', 'console_scripts', 'rshell')()
  File "/usr/local/lib/python3.7/site-packages/rshell/command_line.py", line 4, in main
    rshell.main.main()
  File "/usr/local/lib/python3.7/site-packages/rshell/main.py", line 2712, in main
    real_main()
  File "/usr/local/lib/python3.7/site-packages/rshell/main.py", line 2674, in real_main
    connect(args.port, baud=args.baud, wait=args.wait, user=args.user, password=args.password)
  File "/usr/local/lib/python3.7/site-packages/rshell/main.py", line 1192, in connect
    connect_serial(port, baud=baud, wait=wait)
  File "/usr/local/lib/python3.7/site-packages/rshell/main.py", line 1216, in connect_serial
    dev = DeviceSerial(port, baud, wait)
  File "/usr/local/lib/python3.7/site-packages/rshell/main.py", line 1462, in __init__
    Device.__init__(self, pyb)
  File "/usr/local/lib/python3.7/site-packages/rshell/main.py", line 1269, in __init__
    elif not self.remote_eval(test_unhexlify):
  File "/usr/local/lib/python3.7/site-packages/rshell/main.py", line 1379, in remote_eval
    return eval(self.remote(func, *args, **kwargs))
  File "/usr/local/lib/python3.7/site-packages/rshell/main.py", line 1357, in remote
    self.pyb.enter_raw_repl()
  File "/usr/local/lib/python3.7/site-packages/rshell/pyboard.py", line 187, in enter_raw_repl
    raise PyboardError('could not enter raw repl')
rshell.pyboard.PyboardError: could not enter raw repl
```

### CPU Halted, lol

```
/Users/ariestiyansyah/code/research/github/ariestiyansyah/esp32/fitra> repl
Entering REPL. Use Control-X to exit.
repl_serial_to_stdout dev = <rshell.main.DeviceSerial object at 0x102a58cc0>
>
MicroPython ESP32_LoBo_v3.2.24 - 2018-09-06 on ESP32 Rizky with ESP32
Type "help()" for more information.
>>>
>>> import machine
>>> np = machine.Neopixel(machine.Pin(13), 24)
>>> np.deinit()
>>> np = machine.Neopixel(machine.Pin(13), 24)
Guru Meditation Error: Core  1 panic'ed (LoadProhibited). Exception was unhandled.
Core 1 register dump:
PC      : 0x400e0027  PS      : 0x00060031  A0      : 0x800e01a8  A1      : 0x3ffb1fb0
A2      : 0x00000018  A3      : 0x00000000  A4      : 0x00000000  A5      : 0x00000000
A6      : 0x00000000  A7      : 0x00000004  A8      : 0x0ffd114c  A9      : 0x00000000
A10     : 0x00000009  A11     : 0x00000000  A12     : 0x00002000  A13     : 0x3ff44024
A14     : 0x00000000  A15     : 0x00060923  SAR     : 0x0000000b  EXCCAUSE: 0x0000001c
EXCVADDR: 0x00000018  LBEG    : 0x4000c28c  LEND    : 0x4000c296  LCOUNT  : 0x00000000
Core 1 was running in ISR context:
EPC1    : 0x400e0027  EPC2    : 0x00000000  EPC3    : 0x00000000  EPC4    : 0x40083410

Backtrace: 0x400e0027:0x3ffb1fb0 0x400e01a5:0x3ffb1fe0 0x40082779:0x3ffb2010 0x400e03ef:0x00000000

CPU halted.

serial port pyboard closed
```
