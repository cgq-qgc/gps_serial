#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'xmalet'
__date__ = '2016-04-25'
__description__ = " "
__version__ = '1.0'
import re

import pynmea2
import serial
from pynmea2 import types
from serial.tools import list_ports, list_ports_common


class GpsInfo(object):
    def __init__(self, data: pynmea2.types.GGA = None, lat=None, long=None, altitude=None, srid=4326, nb_sats=0,
                 gps_qual=0, geo_sep_units=0):
        if data is None:
            self.latitude = lat
            self.longitude = long
            self.altitude = altitude
            self.srid = srid
            self.nb_satelites = nb_sats
            self.gps_qual = gps_qual
            self.geo_sep_units = geo_sep_units
        else:
            self.latitude = data.latitude
            self.longitude = data.longitude
            self.altitude = data.altitude
            self.altitude_units = data.altitude_units
            self.srid = srid
            self.nb_satelites = data.num_sats
            self.gps_qual = data.gps_qual
            self.geo_sep_units = data.geo_sep_units

    def __str__(self):
        return """"Coordinates :
        latitude: {}
        longitude: {}
        altitude: {} {}
        number of satellite: {}
        GPS Signal Quality: {}
        System Units: {}""".format(self.latitude, self.longitude, self.altitude, self.altitude_units, self.nb_satelites,
                                   self.gps_qual, self.geo_sep_units)


class GpsUsbReceiver(object):
    def __init__(self):
        self.port = None
        self.usb_ports = None
        self.get_usb_port()

    def get_usb_port(self):
        self.usb_ports = []
        for ports in list_ports.comports():
            print(ports)
            if re.search(r".*usb.*", ports.description.lower()):
                print(ports)
                serial_port = serial.Serial(ports.device, baudrate=4800, timeout=1)
                self.usb_port_is_gps(serial_port)
                self.usb_ports.append(serial_port)

    def usb_port_is_gps(self, usb_port: serial.Serial):
        while 1:
            try:
                data = usb_port.readline().decode('ascii')
                # nmea = pynmea2.parse(usb_port.readline().decode('ascii'))
                streamreader = pynmea2.NMEAStreamReader()
                for msg in streamreader.next(data):
                    print(type(msg))
                    print(msg)
                    if isinstance(msg, pynmea2.types.talker.GGA):
                        print(GpsInfo(data=msg))
            except KeyboardInterrupt:
                import sys
                sys.exit()
            except pynmea2.ParseError as s:
                print(s)
            except AttributeError:
                pass
            except Exception as e:
                print(e)


if __name__ == '__main__':
    GpsUsbReceiver()
