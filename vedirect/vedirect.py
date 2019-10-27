import serial

"""
# VE.Direct parser inspired by https://github.com/karioja/vedirect/blob/master/vedirect.py
"""
class Vedirect:

    # The error code of the device (relevant when the device is in the fault state).
    #
    # Error 19 can be ignored, this condition regularly occurs during start-up or shutdown of the MPPT charger.
    # Since version 1.15 this error will no longer be reported.
    #
    # Error 21 can be ignored for 5 minutes, this condition regularly occurs during start-up or shutdown
    # of the MPPT charger. Since version 1.16 this warning will no longer be reported when it is not persistent.
    #
    VICTRON_ERROR = {
        '0': 'No error',
        '2': 'Battery voltage too high',
        '17': 'Charger temperature too high',
        '18': 'Charger over current',
        '19': 'Charger current reversed',
        '20': 'Bulk time limit exceeded',
        '21': 'Current sensor issue',
        '26': 'Terminals overheated',
        '28': 'Converter issue',  # (dual converter models only)
        '33': 'Input voltage too high (solar panel)',
        '34': 'Input current too high (solar panel)',
        '38': 'Input shutdown (excessive battery voltage)',
        '39': 'Input shutdown (due to current flow during off mode)',
        '65': 'Lost communication with one of devices',
        '66': 'Synchronised charging device configuration issue',
        '67': 'BMS connection lost',
        '68': 'Network misconfigured',
        '116': 'Factory calibration data lost',
        '117': 'Invalid/incompatible firmware',
        '119': 'User settings invalid'
    }

    # The state of operation
    VICTRON_CS = {
        '0': 'Off',
        '2': 'Fault',
        '3': 'Bulk',
        '4': 'Absorption',
        '5': 'Float',
        '7': 'Equalize (manual)',
        '245': 'Starting-up',
        '247': 'Auto equalize / Recondition',
        '252': 'External control'
    }

    # The possible values for the tracker operation
    VICTRON_MTTP = {
        '0': 'Off',
        '1': 'Limited',
        '2': 'Active'
    }

    # Off reason, this field described why a unit is switched off.
    #
    # Available on SmartSolar mppt chargers since firmware version v1.44 (VE.Direct models)
    # and v1.03 (SmartSolar VE.Can models)
    # FIXME: This might not work as a dictionary
    VICTRON_OFF_REASON = {
        "0x00000001": "No input power",
        "0x00000002": "Switched off (power switch)",
        "0x00000004": "Switched off (device mode register)",
        "0x00000008": "Remote input",
        "0x00000010": "Protection active",
        "0x00000020": "Paygo",
        "0x00000040": "BMS",
        "0x00000080": "Engine shutdown detection",
        "0x00000100": "Analysing input voltage"
    }

    def __init__(self, port='/dev/ttyAMA0', timeout=5):
        """
        Initialise serial component of the Victron parser. Default value is the standard serial port on Raspberry pi
        :param port:
        :param timeout:
        """
        self.ser = serial.Serial(port, 19200, timeout=timeout)
        self.header1 = b'\r'
        self.header2 = b'\n'
        self.delimiter = b'\t'
        self.key = bytearray()
        self.value = bytearray()
        self.bytes_sum = 0
        self.state = self.wait_header
        self.dict = {}

    wait_header, in_key, in_value, in_checksum = range(4)

    def input(self, byte):

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
                if self.key.decode() == 'Checksum':
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
                self.dict[self.key.decode()] = self.value.decode()
                self.key = bytearray()
                self.value = bytearray()
            else:
                self.value += byte

            return None

        elif self.state == self.in_checksum:
            self.bytes_sum += ord(byte)
            self.key = bytearray()
            self.value = bytearray()
            self.state = self.wait_header
            if self.bytes_sum % 256 == 0:
                self.bytes_sum = 0
                return self.dict
            else:
                print('Malformed packet')
                self.bytes_sum = 0
        else:
            raise AssertionError()

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