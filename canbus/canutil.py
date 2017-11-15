#!/usr/bin/python

#  python-canbus - An Open Source Python CAN Library 
#  Copyright (c) 2014 Phil Birkelbach
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

# This file contains utiltiy functions for the module.  Some data is 
# automatically generated but can be overridden by the user if necessary.

import glob
import platform

# The following is the configured communications (serial) ports
# These are the defaults for most systems.  Others can simply be
# added as strings to the portlist[] list.  These device names
# should be suitable for use in the pySerial serial.port() property
# This can list every possible port on the machine.  The canbus
# module will test each one to see if it really is a serial port.
portlist = []

system_name = platform.system()
if system_name == "Windows":
    # Scan for available ports.
    for i in range(256):
        available.append(i)
elif system_name == "Darwin":
    # Mac
    portlist.extend(glob.glob('/dev/tty*'))
    portlist.extend(glob.glob('/dev/cu*'))
else:
    # Assume Linux or something else
    portlist.extend(glob.glob('/dev/ttyACM*'))
    portlist.extend(glob.glob('/dev/ttyUSB*'))
    portlist.extend(glob.glob('/dev/ttyS*'))
# Example for manually adding device names.    
#portlist.append('/dev/ttyXYZ123456789')
