import os, shutil, string, tempfile, sys
from xml.dom import minidom 
from optparse import OptionParser

parser = OptionParser(usage="usage: %prog [options] arg", version="%prog 0.1")
parser.add_option("-D", "--debug", action="store", type="int", dest="debug", default="0",
		 help="Set's the level of debuging, 0, 1 or 2")
parser.add_option("-A", "-a", "--All", "--all", action="store_true", dest="All",
		 help="Flag sets whether to run all tests or only the packages specified in args")
parser.add_option("--list", "--List", action="store_true", dest="LIST", default=False,
		 help="Prints the list of all known software packages that can be tested")
parser.add_option("-l", "-L", "--logfile", dest="logfilename",
		 help="specify location of the logfile else log file is " + tempfile.gettempdir() + "/apptester.log")


(options, args) = parser.parse_args()

if options.debug == 0:
  print "no debug"
  os.environ.__setitem__("WINEDEBUG", 'WINEDEBUG=""')

elif options.debug == 1:
  print "Some debug"
  os.environ.__setitem__("WINEDEBUG", 'WINEDEBUG="+trace"')

elif options.debug == 2:
  print "Lots and Lots"
  os.environ.__setitem__("WINEDEBUG", 'WINEDEBUG="+all"')

else:
  sys.exit("Please set a proper debug value")



#
#print os.environ["HOME"]
#print os.environ.get("HOME")
#os.environ.__setitem__("HOME", "test")
#print os.environ["HOME"]
#print os.environ.get("HOME")
#
#os.environ.__setitem__("WINESERVER", "wineserver")
#print os.environ["WINESERVER"]
#wns = os.environ["WINESERVER"] + " -k"
#print wns
#
#print os.environ["PATH"]


#shutil.move("test", 
#for file in os.listdir("test"):
#     shutil.move(os.path.join("test",file),os.getcwd())



#xmldoc = minidom.parse('packages/firefox.xml') 
#reflist = xmldoc.getElementsByTagName('install')      
#bitref = reflist[0]
#a = bitref.attributes["cmd"]

#SOFTWARE="software"
#print a.value
#print a.value.replace("%SOFTWARE%",SOFTWARE)

