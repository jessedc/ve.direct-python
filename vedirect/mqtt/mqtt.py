#!/usr/bin/python -u
# -*- coding: utf-8 -*-

import argparse
from vedirect.vedirect import Vedirect
import paho.mqtt.client as mqtt

victron_key_map = {
    'LOAD': 'now/battery-state',
    'H19': 'total/yield',
    'VPV': 'now/pv-voltage',
    'ERR': 'now/error',
    'FW': 'system/firmware',
    'I': 'now/battery-current',
    'H21': 'now/max-power',
    'IL': 'now/load-current',
    'PID': 'system/pid',
    'H20': 'now/yield',
    'H23': 'yesterday/max-power',
    'MPPT': 'now/mppt-state',
    'HSDS': 'system/day-seq',
    'SER#': 'system/serial-no',
    'V': 'now/battery-voltage',
    'CS': 'now/state',
    'H22': 'yesterday/yield',
    'PPV': 'now/pv-power'
}

class Connector:

    def __init__(self, broker, client_id, mqtt_user=None, mqtt_password=None, base_topic='victron/mppt/', serial='/dev/ttyAMA0'):
        self.base_topic = base_topic

        self.mqttc = mqtt.Client(client_id)
        if mqtt_user is not None and mqtt_password is not None:
            self.mqttc.username_pw_set(mqtt_user, mqtt_password)
        self.mqttc.connect(broker)
        self.mqttc.loop_start()

        self.ve = Vedirect(serial, 1)
        self.ve.read_data_callback(self.on_victron_data_callback)

    # Local variable to store previous frame
    # previous_victron_frame = {}

    def on_victron_data_callback(self, data):
        # global previous_victron_frame

        for key, value in data.iteritems():
            # NB: To filter values, do something like this:
            # if previous_victron_frame.get(key, None) == value:
            #     continue
            # else:
            #     previous_victron_frame[key] = value

            if key == 'CS':
                value = Vedirect.VICTRON_CS[value]
            elif key == 'MPPT':
                value = Vedirect.VICTRON_CS[value]
            elif key == 'ERR':
                value = Vedirect.VICTRON_ERROR[value]

            key = self.base_topic + victron_key_map[key]
            self.mqttc.publish(key, value)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Parse Ve.Direct serial data onto MQTT broker')
    parser.add_argument('--broker', help='Broker IP address', required=True)
    parser.add_argument('--client-id', help='Unique mqtt client id', required=True)
    parser.add_argument('--username', help='Username for mqtt broker')
    parser.add_argument('--password', help='Password for mqtt broker')
    args = parser.parse_args()

    connector = Connector(args.broker, args.client_id, args.username, args.password)
