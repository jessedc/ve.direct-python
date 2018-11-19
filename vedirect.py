
# Inspired by
# https://github.com/karioja/vedirect/blob/master/vedirect.py

import serial


class Vedirect:

    def __init__(self, port, timeout):
        self.serialport = port
        self.ser = serial.Serial(port, 19200, timeout=timeout)
        self.header1 = '\r'
        self.header2 = '\n'
        self.delimiter = '\t'
        self.hexmarker = ':'
        self.key = ''
        self.value = ''
        self.bytes_sum = 0
        self.state = self.wait_header
        self.dict = {}

    hex, wait_header, in_key, in_value, in_checksum = range(5)

    def input(self, byte):
        if byte == self.hexmarker and self.state != self.in_checksum:
            self.state = self.hex

        if self.state == self.wait_header:
            self.bytes_sum += ord(byte)
            if byte == self.header1:
                self.state = self.wait_header
            elif byte == self.header2:
                self.state = self.in_key

            return None

        elif self.state == self.in_key:
            self.bytes_sum += ord(byte)
            if byte == self.delimiter:
                if self.key == 'Checksum':
                    self.state = self.in_checksum
                else:
                    self.state = self.in_value
            else:
                self.key += byte

            return None

        elif self.state == self.in_value:
            self.bytes_sum += ord(byte)
            if byte == self.header1:
                self.state = self.wait_header
                self.dict[self.key] = self.value
                self.key = ''
                self.value = ''
            else:
                self.value += byte

            return None

        elif self.state == self.in_checksum:
            self.bytes_sum += ord(byte)
            self.key = ''
            self.value = ''
            self.state = self.wait_header
            if self.bytes_sum % 256 == 0:
                self.bytes_sum = 0
                return self.dict
            else:
                print 'Malformed packet'
                self.bytes_sum = 0

        elif self.state == self.hex:
            self.bytes_sum = 0
            if byte == self.header2:
                self.state = self.wait_header

        else:
            raise AssertionError()

    def read_data(self):
        while True:
            byte = self.ser.read(1)
            packet = self.input(byte)

    def read_data_single(self):
        while True:
            byte = self.ser.read(1)
            packet = self.input(byte)
            if packet is not None:
                return packet

    def read_data_callback(self, callback):
        while True:
            byte = self.ser.read(1)
            if byte:
                packet = self.input(byte)
                if packet is not None:
                    callback(packet)
            else:
                break
