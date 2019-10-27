#!/bin/bash

if [ ! -f .env.installed ]; then
    cp .env.example .env.installed
fi

cp ./lib/systemd/system/vedirect.service /lib/systemd/system/
chmod 644 /lib/systemd/system/vedirect.service

# TODO: Re-enable CPU-temperature
#cp ./lib/systemd/system/cputemp.service /lib/systemd/system/
#chmod 644 /lib/systemd/system/cputemp.service

systemctl daemon-reload
#systemctl enable cputemp.service
systemctl enable vedirect.service
