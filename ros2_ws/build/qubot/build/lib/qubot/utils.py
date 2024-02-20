#! /home/qubot/.pyenv/shims/python3
import serial
import struct
import time
import threading
class PCB():
    def __init__(
            self,        
            port="/dev/ttyUSB0",
            baudrate = 115200):

        self.ser = serial.Serial(port=port, baudrate=baudrate)
        self.magnetic_field_spherical = [0.,0.,0.]
        if not self.ser.is_open:
            self.ser.open()
        print(str(self.ser.is_open))

    def PCB_read(self):
        # count = 0
        # time0 = time.time()
        while True:
            if self.ser.in_waiting >0:
                value = self.ser.read(60)
                # time1 = time.time()
                # print('time:',time1-time0)
                if value[2] == 1:
                    # magnetic field
                    self.magnetic_field_spherical[0] = struct.unpack('f',value[8:12])[0]
                    self.magnetic_field_spherical[1] = struct.unpack('f',value[12:16])[0]
                    self.magnetic_field_spherical[2] = struct.unpack('f',value[16:20])[0]
            
                # count += 1
                # print(count)
                # print(self.magnetic_amp,self.magnetic_theta,self.magnetic_phi)