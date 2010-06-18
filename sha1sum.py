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

import os, os.path, hashlib, string, sys

if (len(sys.argv) < 2 ):
	print "Usage: " + sys.argv[0] + " path you wish to sha1sum " + " [path to save output to] "
	print "Saving to file is optional, if no path is given then sha1sum(s) are printed to stdout"

if (len(sys.argv) == 3 ):
 if os.path.isfile( sys.argv[2] ):
    os.remove(sys.argv[2])
 class Logger(object):
    def __init__(self):
        self.terminal = sys.stdout
        self.log = []

    def write(self, message):
        self.terminal.write(message)
        self.log.append(message)  

sys.stdout = Logger()

for dirname in sys.argv[1:]:
   for root, dirs, files in os.walk(dirname):
     for name in dirs:
	 if os.path.relpath(root) == ".":
	  print "CHECK_DIR(\"" + name.replace(" ","` ") + "\")"
	 else:
	  print "CHECK_DIR(\"" + os.path.relpath(root).replace(" ","` ") + "\\"  + name.replace(" ","` ") + "\")"
     for name in files:
       try: 
	 f = open(os.path.join(root, name), "rb")
  	 h = hashlib.sha1()
  	 h.update(f.read())
 	 filehash = h.hexdigest()
 	 f.close()
	 if os.path.relpath(root) == ".":
	  print "SHA1(\"" +filehash.lower() + "\", \"" + name.replace(" ","` ") + "\")"
	 else:
	  print "SHA1(\"" +filehash.lower() + "\", \"" + os.path.relpath(root).replace(" ","` ") + "/" + name.replace(" ","` ") + "\")"
       except IOError:
	 print "sha1sum.py unable to open file " + os.path.join(root, name)
	 sys.exit(-1)
       except:
	 print "sha1sum.py encountered an unexpected error"
	 sys.exit(-1)

logfile = open(sys.argv[2], "a")
for item in sys.stdout.log:
  logfile.write(str(item))

# all files hashed with success
sys.exit(0)
