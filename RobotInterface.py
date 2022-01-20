# @ Droid Group: Lonnie Gasque, Austin Hetherington, & Ibrahim Salman
import serial
import time
import struct
import math


class robotConnection:
        def __init__(self):
            self.connection = serial.Serial('/dev/ttyUSB0',baudrate=115200)
        def open(self):
                self.connection.open()
                time.sleep(0.0125)
        def write(self,s):
                self.connection.write(s)
                time.sleep(0.0125)
        def read(self,n):
                return self.connection.read(n)
                time.sleep(0.0125)
        def close(self):
                self.connection.close()
                time.sleep(0.0125)
        def start(self):
                self.write(chr(128))
                time.sleep(0.0125)
        def reset(self):
                self.write(chr(7))
                time.sleep(0.0125)
        def stop (self):
                self.write(chr(173))
        def passive(self):
                self.write(chr(128))
                time.sleep(0.0125)
        def safe(self):
                self.write(chr(131))
                time.sleep(0.0125)
        def full(self):
                self.write(chr(132))
                time.sleep(0.0125)
        #returns true if clean button is pressed
        def readButton(self):
                self.write(chr(142)+chr(18))
                time.sleep(0.0125)
                rawData = self.read(1)
                byte = struct.unpack('B',rawData)
                return bool(byte[0]&0x01)
                
        #function that returns true if right bumber is pressed
        def readBumpRight(self):
                self.write(chr(142)+chr(7))
                time.sleep(0.0125)
                rawData = self.read(1)
                byte = struct.unpack('B',rawData)[0]
                return bool(byte&0x01)
        #function that returns true if left bumber is pressed
        def readBumpLeft(self):
                self.write(chr(142)+chr(7))
                time.sleep(0.0125)
                rawData = self.read(1)
                byte = struct.unpack('B',rawData)[0]
                return bool(byte&0x02)
        #function that returns true if right wheel is dropped
        def readWheelDropRight(self):
                self.write(chr(142)+chr(7))
                time.sleep(0.0125)
                rawData = self.read(1)
                byte = struct.unpack('B',rawData)[0]
                return bool(byte&0x04)
        #function that returns true if left wheel is dropped
        def readWheelDropLeft(self):
                self.write(chr(142)+chr(7))
                time.sleep(0.0125)
                rawData = self.read(1)
                byte = struct.unpack('B',rawData)[0]
                return bool(byte&0x08)
        #function that returns true if left cliff sensor is activated
        def readCliffLeft(self):
                self.write(chr(142)+chr(9))
                time.sleep(0.0125)
                rawData = self.read(1)
                byte = struct.unpack('B',rawData)[0]
                return bool(byte&0x01)
        #function that returns true if left front cliff sensor is activated
        def readCliffFrontLeft(self):
                self.write(chr(142)+chr(10))
                time.sleep(0.0125)
                rawData = self.read(1)
                byte = struct.unpack('B',rawData)[0]
                return bool(byte&0x01)
        #function that returns true if right front cliff sensor is activated
        def readCliffFrontRight(self):
                self.write(chr(142)+chr(11))
                time.sleep(0.0125)
                rawData = self.read(1)
                byte = struct.unpack('B',rawData)[0]
                return bool(byte&0x01)
        #function that returns true if right cliff sensor is activated
        def readCliffRight(self):
                self.write(chr(142)+chr(12))
                time.sleep(0.0125)
                rawData = self.read(1)
                byte = struct.unpack('B',rawData)[0]
                return bool(byte&0x01)
        def readVirtualWall(self):
                self.write(chr(142)+chr(13))
                time.sleep(0.0125)
                rawData = self.read(1)
                byte = struct.unpack('B',rawData)[0]
                return bool(byte&0x01)
        def drive(self, velocity, radius):
                byte = struct.pack('>B2h',137,velocity,radius)
                self.write(byte)
        def warningSong(self):
                self.write(chr(140)+chr(0)+chr(9)+chr(55)+chr(64)+chr(48)+chr(64)+chr(51)+chr(16)+chr(53)+chr(16)+chr(55)+chr(64)+chr(48)+chr(64)+chr(51)+chr(16)+chr(53)+chr(16)+chr(50)+chr(64))
                time.sleep(0.0125)       
        def successSong1(self):
                self.write(chr(140)+chr(1)+chr(6)+chr(40)+chr(16)+chr(45)+chr(16)+chr(50)+chr(16)+chr(55)+chr(16)+chr(59)+chr(16)+chr(64)+chr(16))
                time.sleep(0.0125) 
        def successSong2(self):
                self.write(chr(140)+chr(2)+chr(6)+chr(40)+chr(16)+chr(45)+chr(19)+chr(50)+chr(16)+chr(55)+chr(16)+chr(59)+chr(16)+chr(64)+chr(16))
                time.sleep(0.0125)               
        def song1(self):
                self.write(chr(141)+chr(0))
        def song2(self):
                self.write(chr(141)+chr(1)) 
        def song3(self):
                self.write(chr(141)+chr(2))                      
        def angle(self):
                self.write(chr(142)+chr(20))
                time.sleep(0.0125)
                rawData = self.read(2)
                byte = struct.unpack('>h',rawData)[0]
                return byte
        def distance(self):
                self.write(chr(142)+chr(19))
                time.sleep(0.0125)
                rawData = self.read(2)
                byte = struct.unpack('>h',rawData)[0]
                return byte
        def driveDirect(self, velocityLeft, velocityRight):
                byte = struct.pack('>B2h',145,velocityRight,velocityLeft)
                self.write(byte)

        def readVirtualWall(self):
                self.write(chr(142)+chr(13))
                time.sleep(0.0125)
                rawData = self.read(1)
                byte = struct.unpack('B',rawData)[0]
                return bool(byte&0x01)
        def readIrOmni(self):
                self.write(chr(142)+chr(17))
                rawData = self.read(1)
                byte = struct.unpack('B',rawData)[0]
                return byte
        def readLightRight(self):
                self.write(chr(142)+chr(51))
                rawData = self.read(2)
                byte = struct.unpack('>H',rawData)[0]
                return math.sqrt(byte)
        def readLightFrontRight(self):
                self.write(chr(142)+chr(50))
                rawData = self.read(2)
                byte = struct.unpack('>H',rawData)[0]
                return math.sqrt(byte)
        def readLightCenterRight(self):
                self.write(chr(142)+chr(49))
                rawData = self.read(2)
                byte = struct.unpack('>H',rawData)[0]
                return math.sqrt(byte)
        def readRightIR(self):
                self.write(chr(142)+chr(53))
                rawData = self.read(1)
                byte = struct.unpack('B',rawData)[0]
                return byte       
        def readLeftIR(self):
                self.write(chr(142)+chr(52))
                rawData = self.read(1)
                byte = struct.unpack('B',rawData)[0]
                return byte 
        def readDock(self):
                self.write(chr(142)+chr(34))
                rawData = self.read(1)
                byte = struct.unpack('b',rawData)[0]
                return byte
        def readCharging(self):
                self.write(chr(142)+chr(21))
                rawData = self.read(1)
                byte = struct.unpack('B',rawData)[0]
                return byte
                                                                           