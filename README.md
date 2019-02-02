# VEDirect Serial

Designed for Raspberry Pi, collects serial data from serial port (GPIO 14 + 15 ) parses serial output from the Victron VE.Direct port and pipes it to a MQTT broker.

# Installation

This assumes it is installed on a raspberry pi at `/home/pi/serial-reader`

```bash
cp .env.example .env
cp ./lib/systemd/system/vedirect.service /lib/systemd/system/
chmod 644 /lib/systemd/system/vedirect.service
sudo systemctl daemon-reload
sudo systemctl enable vedirect.service
sudo reboot
```

# References

## VE.Direct

Victron Manuals/VE.Direct-Protocol-3.25.pdf

## Systemd
- https://www.raspberrypi-spy.co.uk/2015/10/how-to-autorun-a-python-script-on-boot-using-systemd/
- https://stackoverflow.com/questions/13069634/python-daemon-and-systemd-service
