"""
CLI Entry point
"""
import argparse

from vedirect.influxdb import influx
from vedirect.vedirect import Vedirect
from influxdb import InfluxDBClient

influx_client = None
influx_db = None

def main():
    """
    Invoke the parser
    :return:
    """
    parser = argparse.ArgumentParser(description='Parse VE.Direct serial data')
    parser.add_argument('-i', '--influx', help='Influx DB host')
    parser.add_argument('-d', '--database', help='InfluxDB database')
    parser.add_argument('-p', '--port', help='Serial port')
    args = parser.parse_args()

    global influx_db, influx_client
    influx_client = InfluxDBClient(host=args.influx, port=8086)
    influx_db = args.database

    ve = Vedirect(args.port)
    ve.read_data_callback(on_victron_data_callback)

def on_victron_data_callback(data):
    measurements = influx.measurements_for_packet(data)
    influx_client.write_points(measurements, database=influx_db)

    print(measurements)


if __name__ == "__main__":
    main()