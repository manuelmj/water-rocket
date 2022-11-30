import machine
from time import sleep_ms
import os

from math import atan2,degrees,pi
from struct import unpack as unp


class accel():
    def __init__(self, i2c, addr=0x68):
        self.iic = i2c
        self.addr = addr
        self.iic.start()
        self.iic.writeto(self.addr, bytearray([107, 0]))
        self.iic.stop()

    def get_raw_values(self):
        self.iic.start()
        a = self.iic.readfrom_mem(self.addr, 0x3B, 14)
        self.iic.stop()
        return a

    def get_ints(self):
        b = self.get_raw_values()
        c = []
        for i in b:
            c.append(i)
        return c

    def bytes_toint(self, firstbyte, secondbyte):
        if not firstbyte & 0x80:
            return firstbyte << 8 | secondbyte
        return - (((firstbyte ^ 255) << 8) | (secondbyte ^ 255) + 1)

    def get_values(self):
        raw_ints = self.get_raw_values()
        vals = {}
        vals["AcX"] = self.bytes_toint(raw_ints[0], raw_ints[1])
        vals["AcY"] = self.bytes_toint(raw_ints[2], raw_ints[3])
        vals["AcZ"] = self.bytes_toint(raw_ints[4], raw_ints[5])
        vals["Tmp"] = self.bytes_toint(raw_ints[6], raw_ints[7]) / 340.00 + 36.53
        vals["GyX"] = self.bytes_toint(raw_ints[8], raw_ints[9])
        vals["GyY"] = self.bytes_toint(raw_ints[10], raw_ints[11])
        vals["GyZ"] = self.bytes_toint(raw_ints[12], raw_ints[13])
        return vals  # returned in range of Int16
        # -32768 to 32767

    def pitch_zx(self):
        '''
        Returns pitch angle in degrees based on x and c accelerations.

        '''
        scale = (16384, 8192, 4096, 2048)
        raw = self.get_raw_values()
        x = unp('>h', raw[0:2])[0]/scale[0]
        z = unp('>h', raw[4:6])[0]/scale[0]
        pitch = degrees(pi+atan2(-x,-z))

        if (pitch>=180) and (pitch<=360):
            pitch-=360
        return -pitch

    def pitch_zy(self):
        '''
        Returns pitch angle in degrees based on y and c accelerations.

        '''
        scale = (16384, 8192, 4096, 2048)
        raw = self.get_raw_values()
        y = unp('>h', raw[2:4])[0]/scale[0]
        z = unp('>h', raw[4:6])[0]/scale[0]
        pitch = degrees(pi+atan2(-y,-z))

        if (pitch>=180) and (pitch<=360):
            pitch-=360
        return -pitch

    def val_test(self):  # ONLY FOR TESTING! Also, fast reading sometimes crashes IIC
        from time import sleep
        while 1:
            #print(self.get_values())
            print(self.pitch_zx(),self.pitch_zy())

            sleep_ms(1000)
