#!/usr/bin/python

#Copyright 2010 Seth Shelnutt licensed under the LGPL

# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301, USA

import os, os.path, string, sys, tempfile, xml.dom.minidom
from optparse import OptionParser



parser = OptionParser(usage="usage: %prog [options] arg", version="%prog 0.1")
parser.add_option("-D", "--debug", action="store_true", dest="debug",
		 help="Set whether to print debug info or not")
parser.add_option("-A", "-a", "--All", "--all", action="store_true", dest="All",
		 help="Flag sets whether to run all tests or only the packages specified in args")
parser.add_option("-l", "-L", "--logfile", dest="logfilename",
		 help="specify location of the logfile else log file is " + tempfile.gettempdir() + "/apptester.log")


(options, args) = parser.parse_args()
if len(args) != 1:
    parser.error("Please either use the -A flag or specify a specific software package")

if 'options.logfilename' in globals():
   pass
else:
   options.logfilename = os.path.join( tempfile.gettempdir(), "apptester.log" ) 
if options.debug:
 if os.path.isfile( options.logfilename ):
   os.remove(options.logfilename)
 class Logger(object):
    def __init__(self):
        self.terminal = sys.stdout
        self.log = []

    def write(self, message):
        self.terminal.write(message)
        self.log.append(message)  

sys.stdout = Logger()




