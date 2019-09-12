# VEDirect Serial

Designed for Raspberry Pi, collects serial data from serial port (GPIO 14 + 15 ) parses serial output from the Victron VE.Direct port and pipes it to a MQTT broker.

# Installation

This assumes it is installed on a raspberry pi at `/home/pi/serial-reader`

```bash
cp .env.example .env
sudo cp ./lib/systemd/system/vedirect.service /lib/systemd/system/
sudo chmod 644 /lib/systemd/system/vedirect.service

sudo systemctl daemon-reload
sudo systemctl enable vedirect.service
sudo systemctl start vedirect.service

sudo cp ./lib/systemd/system/cputemp.service /lib/systemd/system/
sudo chmod 644 /lib/systemd/system/cputemp.service

sudo systemctl daemon-reload
sudo systemctl enable cputemp.service
sudo systemctl start cputemp.service

sudo reboot
```

# References

## VE.Direct

Victron Manuals/VE.Direct-Protocol-3.25.pdf

## vcgencmd

- https://medium.com/@kevalpatel2106/monitor-the-core-temperature-of-your-raspberry-pi-3ddfdf82989f
- https://elinux.org/RPI_vcgencmd_usage

## Systemd
- https://www.raspberrypi-spy.co.uk/2015/10/how-to-autorun-a-python-script-on-boot-using-systemd/
- https://stackoverflow.com/questions/13069634/python-daemon-and-systemd-service

## Python

- [Executing periodic actions in Python](https://stackoverflow.com/a/28034554/184130)