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

Connect SparkFun and Rainbow LED WS2812 using jumper by using the following
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
git clone https://github.com/ariestiyansyah/MicroPython_ESP32_psRAM_LoBo.git
```

Config the micropython and build the Firmware
```
cd MicroPython_ESP32_psRAM_LoBo/MicroPython_BUILD/
./BUILD.sh menuconfig
./BUILD.sh
```

Flash it
```
./BUILD.sh flash
```

### Install Gateway

You can follow the instruction from
[https://github.com/mozilla-iot/gateway/blob/master/README.md](https://github.com/mozilla-iot/gateway/blob/master/README.md)
to install Mozilla Gateway in your Raspberry Pi or PC/Mac.

### Web of Things Micropython

Hierarchy of this project

```
.
├── README.md
├── config.example.py
├── config.py
├── connect.py
├── main.py
├── main.py.orig
├── src
│   ├── neopixel
│   │   ├── np.py
│   │   └── np.py.bak
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

### Adding RGB function and Property

Create sample display_odd function to display LED in odd number

```
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

##


