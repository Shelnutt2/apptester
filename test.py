import os, shutil, string
from xml.dom import minidom 

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
for file in os.listdir("test"):
     shutil.move(os.path.join("test",file),os.getcwd())



#xmldoc = minidom.parse('packages/firefox.xml') 
#reflist = xmldoc.getElementsByTagName('install')      
#bitref = reflist[0]
#a = bitref.attributes["cmd"]

#SOFTWARE="software"
#print a.value
#print a.value.replace("%SOFTWARE%",SOFTWARE)

