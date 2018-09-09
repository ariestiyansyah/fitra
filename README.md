# Fitra - Arc Reactor using ESP32 and Web of Things

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

### Flashing Loboris Micropython

Clone the fork of Loboris Micropython repository

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
[https://github.com/mozilla-iot/gateway/blob/master/README.md](https://github.com/mozilla-iot/gateway/blob/master/README.md) to install Mozilla Gateway

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

### Integrate Neopixel

### Adding RGB function and Property

To create new RGB Function simply use the example function

Add property to gateway

### Convert RGB to Hex

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


