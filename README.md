# VE.Direct Python

Python 3 parser for Victron VE.Direct protocol.

This project is designed to run on raspberry pi connected to the VE.Direct port of an MPPT device and then post the data to an influx DB instance.

Raspberry pi serial port is GPIO 14 + 15 and is available at `/dev/ttyAMA0`.

# Installation

- Clone this repository on your raspberry-pi to `/home/pi/ve.direct-pyton`
- Copy `.env.example` to `.env.installed`
- Configure `INFLUX_HOST` and `INFLUX_DB` in `.env.installed`
- Run the `setup.sh`.

```bash
cp .env.example .env.installed
./install.sh
```

Detailed install commands

```
sudo cp ./lib/systemd/system/vedirect.service /lib/systemd/system/
sudo chmod 644 /lib/systemd/system/vedirect.service

sudo systemctl daemon-reload
sudo systemctl enable vedirect.service
sudo systemctl start vedirect.service

sudo reboot
```

# Running the parser directly

```bash
/usr/bin/python3 -u -m vedirect --influx=pi.hole --database=solar --port=/dev/ttyAMA0
```

# Example InfluxDB Measurement

```json
[
    {
      "time": "2019-10-27T01:48:32.729954+00:00", 
      "tags": {
        "sensor": "victron", 
        "location": "outdoors"
      },
      "fields": {"IL": 600, "PPV": 9, "V": 25.7, "I": -270, "VPV": 33.55}, 
      "measurement": "power"
    }, 
    {
      "time": "2019-10-27T01:48:32.729954+00:00", 
      "tags": {
        "sensor": "victron", 
        "location": "outdoors"
      }, 
      "fields": {
        "H21": 25, "H20": 0.07
      }, 
      "measurement": "today"
    },
    {
        "time": "2019-10-27T01:48:32.729954+00:00", 
        "tags": {
          "sensor": "victron",
          "location": "outdoors"
        }, 
        "fields": {
            "MPPT": 2, 
            "CS": 3, 
            "LOAD": 1, 
            "ERR": 0
        }, 
        "measurement": "status"
  }
]
```

# References

## VE.Direct

Victron Manuals/VE.Direct-Protocol-3.27.pdf

VE.Direct parser inspired by https://github.com/karioja/vedirect/blob/master/vedirect.py

## vcgencmd

- https://medium.com/@kevalpatel2106/monitor-the-core-temperature-of-your-raspberry-pi-3ddfdf82989f
- https://elinux.org/RPI_vcgencmd_usage

## Systemd

- https://www.raspberrypi-spy.co.uk/2015/10/how-to-autorun-a-python-script-on-boot-using-systemd/
- https://stackoverflow.com/questions/13069634/python-daemon-and-systemd-service

## Python

- [Executing periodic actions in Python](https://stackoverflow.com/a/28034554/184130)