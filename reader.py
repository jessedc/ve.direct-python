#!/usr/bin/python -u
# -*- coding: utf-8 -*-

import argparse
from vedirect import Vedirect
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

victron_state = {
    '0': 'Off',
    '2': 'Fault',
    '3': 'Bulk',
    '4': 'Absorption',
    '5': 'Float'
}

mppt_state = {
    '0': 'Off',
    '1': 'Limited',
    '2': 'Active'
}

victron_error = {
    '0': 'No error [error 0]',
    '2': 'Battery voltage too high [error 2]',
    '17': 'Charger temperature too high [error 17]',
    '18': 'Charger over current [error 18]',
    '19': 'Charger current reversed [error 19]',
    '20': 'Bulk time limit exceeded [error 20]',
    '21': 'Current sensor issue [error 21]',
    '26': 'Terminals overheated [error 26]',
    '33': 'Input voltage too high (solar panel) [error 33]',
    '34': 'Input current too high (solar panel) [error 34]',
    '38': 'Input shutdown (excessive battery voltage) [error 38]',
    '116': 'Factory calibration data lost [error 116]',
    '117': 'Invalid/incompatible firmware [error 117]',
    '119': 'User settings invalid [error 119]'
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
                value = victron_state[value]
            elif key == 'MPPT':
                value = mppt_state[value]
            elif key == 'ERR':
                value = victron_error[value]

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
