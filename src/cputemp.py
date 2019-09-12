#!/usr/bin/python -u
# -*- coding: utf-8 -*-

import argparse
import os
import paho.mqtt.client as mqtt
import re
import time

# simple global regex for parsing the vcgencmd response
re_tmp = re.compile('temp=([0-9.]{3,})\'C\\n')


def do_every(period, f, *args):
    def g_tick():
        t = time.time()
        count = 0
        while True:
            count += 1
            yield max(t + count * period - time.time(), 0)
    g = g_tick()
    while True:
        time.sleep(next(g))
        f(*args)


class Connector:
    def __init__(self, broker, client_id, base_topic, mqtt_user=None, mqtt_password=None):
        self.base_topic = base_topic

        self.mqttc = mqtt.Client(client_id)
        if mqtt_user is not None and mqtt_password is not None:
            self.mqttc.username_pw_set(mqtt_user, mqtt_password)

        self.mqttc.connect(broker)
        self.mqttc.loop_start()

    def measure_temp(self):
        return re_tmp.match(os.popen("vcgencmd measure_temp").readline()).group(1)

    def report_temp(self):
        key = self.base_topic + 'cpu'
        self.mqttc.publish(key, self.measure_temp())


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Parse Ve.Direct serial data onto MQTT broker')
    parser.add_argument('--broker', help='Broker IP address', required=True)
    parser.add_argument('--client-id', help='Unique mqtt client id', required=True)
    parser.add_argument('--username', help='Username for mqtt broker')
    parser.add_argument('--password', help='Password for mqtt broker')
    parser.add_argument('--topic', help='Base topic eg. pi/solar', default='pi/solar/')
    parser.add_argument('--report-period', help='Frequency of reporting to the mqtt broker', default=5)
    args = parser.parse_args()

    connector = Connector(args.broker, args.client_id, args.topic, args.username, args.password)

    temp = connector.measure_temp()
    period = int(args.report_period)
    print "Temperature: " + temp + ". Reporting every " + args.report_period + " seconds."
    do_every(period, connector.report_temp)
