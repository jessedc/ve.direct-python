#!/usr/bin/python -u
# -*- coding: utf-8 -*-

import argparse
import os
import paho.mqtt.client as mqtt
import re

# simple global regex for parsing the vcgencmd response
re_tmp = re.compile('temp=([0-9.]{3,}\'C)\\n')


class Connector:
    def __init__(self, broker, client_id, mqtt_user=None, mqtt_password=None, base_topic='raspberry-pi/mppt/', serial='/dev/ttyAMA0'):
        self.base_topic = base_topic

        self.mqttc = mqtt.Client(client_id)
        if mqtt_user is not None and mqtt_password is not None:
            self.mqttc.username_pw_set(mqtt_user, mqtt_password)

        self.mqttc.connect(broker)
        self.mqttc.loop_start()

    def measure_temp(self):
        return re_tmp.match(os.popen("vcgencmd measure_temp").readline()).group(1)

    def report_temp(self, temp):
        key = self.base_topic + 'cpu'
        self.mqttc.publish(key, temp)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Parse Ve.Direct serial data onto MQTT broker')
    parser.add_argument('--broker', help='Broker IP address', required=True)
    parser.add_argument('--client-id', help='Unique mqtt client id', required=True)
    parser.add_argument('--username', help='Username for mqtt broker')
    parser.add_argument('--password', help='Password for mqtt broker')
    args = parser.parse_args()

    connector = Connector(args.broker, args.client_id, args.username, args.password)

    temp = connector.measure_temp()
    print "Temperature: " + temp

    connector.report_temp(temp)
