#  CAN-FIX Utilities - An Open Source CAN FIX Utility Package 
#  Copyright (c) 2012 Phil Birkelbach
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.

from exceptions import *
import socket
import canbus


class Adapter():
    """Class that represents a generic TCP/IP to CAN Bus Adapter"""
    def __init__(self):
        self.name = "CANFIX Network Adapter"
        self.shortname = "network"
        self.type = "network"
        # Statistics and counters
        self.sentFrames = 0
        self.recvFrames = 0
        self.errors = 0
        self.lasterror = None
    
    def __readResponse(self, ch):
        s = ""

        while 1:
            try:
                #TODO: This is probably not very efficient but
                # having a buffer bigger than 1 allows for
                # multiple frames.  Need to handle that
                x = self.socket.recv(1)
            except socket.timeout:
                raise DeviceTimeout
            else:
                s = s + x
                if s[-1] == '\n':
                    if s[0] == ch.lower(): # Good Response
                        return s
                    if s[0] == "*": # Error
                        self.lasterror = s[1]
                        self.errors += 1
                        
    def __sendCommand(self, command):
        if command[-1] != '\n':
            command = command + '\n'
        self.socket.send(command)
        
    def connect(self, config):
        try:
            self.bitrate = config.bitrate
        except KeyError:
            self.bitrate = 125
        bitrates = {125:"B125\n", 250:"B250\n", 500:"B500\n", 1000:"B1000\n"}
        try:
            self.host = config.ipaddress
        except KeyError:
            self.host = "127.0.0.1"
        try:
            self.port = config.port
        except KeyError:
            self.port = 63349
        try:
            self.timeout = config.timeout
        except KeyError:
            self.timeout = 0.25
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.settimeout(self.timeout)
            self.socket.connect((self.host, self.port))
            print "Setting Bit Rate"
            self.__sendCommand(bitrates[self.bitrate])
            self.open()
        except BusReadError:
            raise BusInitError("Unable to Initialize CAN Port")
    
    def disconnect(self):
        self.close()

    def open(self):
        print "Opening CAN Port"
        self.__sendCommand("O")
        
    def close(self):
        print "Closing CAN Port"
        self.__sendCommand("C")
        self.socket.close()

    def error(self):
        return self.errors

    def sendFrame(self, frame):
        if frame.id < 0 or frame.id > 2047:
            raise ValueError("Frame ID out of range")
        xmit = "W"
        xmit = xmit + '%03X' % frame.id
        xmit = xmit + ':'
        for each in frame.data:
            xmit = xmit + '%02X' % each
        xmit = xmit + '\n'
        self.sentFrames += 1
        self.__sendCommand(xmit)
        
    def recvFrame(self):
        result = self.__readResponse("R")
        
        if result[0] != 'r':
            raise BusReadError("Unknown response from Adapter")
        data= []
        for n in range((len(result)-5)/2):
            data.append(int(result[5+n*2:7+n*2], 16))
        frame = canbus.Frame(int(result[1:4], 16), data)
        self.recvFrames += 1
        return frame