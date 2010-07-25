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

import os, os.path, string, sys, tempfile, datetime, subprocess, hashlib, urllib, shutil, time
from optparse import OptionParser
from xml.dom import minidom 


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

class Logger(object):
    def __init__(self):
        self.terminal = sys.stdout
        self.log = []

    def write(self, message):
        self.terminal.write(message)
        self.log.append(message)  

sys.stdout = Logger()

if len(args) != 1 and not any( [options.LIST, options.All] ):
    parser.error("Please either use the -A flag or specify a specific software package")


def cleanup():
  if os.path.exists(WINEPREFIX):
     shutil.rmtree(WINEPREFIX)
  if os.path.exists(APPINSTALL_CACHE):
     CACHEFILES = os.listdir(APPINSTALL_CACHE)
     for File in CACHEFILES:
         if any( [File == "*.txt", File == "*.ahk", File == "helper_functions*", File == "init_tests*", File == "test_list*"] ):
	    os.remove(os.path.join(WINEPREFIX, File))
  return

def prep_prefix():
  wns = WINESERVER + " -k"
  wnsp = subprocess.Popen(wns, shell=True)
  if os.path.exists(WINEPREFIX):
    shutil.rmtree(WINEPREFIX)
  winerun("wineboot")
  ln = "ln -s " + APPINSTALL_CACHE +" " + WINEPREFIX + "/drive_c/appinstall"
  lnp = subprocess.Popen(ln, shell=True)
  return

def verifysha1(PATH,SHA1):
  f = open(PATH, "rb")
  h = hashlib.sha1()
  h.update(f.read())
  filehash = h.hexdigest()
  f.close()
  if filehash.lower() != SHA1:
     sys.exit( "SHA1SUM of " + PATH + " failed.")
  return

def reports(package, message):
#  if not os.path.exists("pappinstall-" + TAG):
  if not os.path.exists("pappinstall-" + TAG):
   os.mkdir("pappinstall-" + TAG)
   f = open(os.path.join("pappinstall-" + TAG,package + ".report"), 'a')
  else:
   f = open(os.path.join("pappinstall-" + TAG,package + ".report"), 'a')
  f.write(str(message) + '\n')
  f.close()

def which(program):
    def is_exe(fpath):
        return os.path.exists(fpath) and os.access(fpath, os.X_OK)

    fpath, fname = os.path.split(program)
    if fpath:
        if is_exe(program):
            return program
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return exe_file

    return None


def winerun(progs):
    wp = WINEDEBUG + " " + WINE + " " + progs
    wpp = subprocess.Popen(wp, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout_value, stderr_value = wpp.communicate()
    wpp.wait()
    return stdout_value, stderr_value

def wineconsolerun(progs):
    wcp = WINEDEBUG + " " + WINECONSOLE + " " + progs
    wcpp = subprocess.Popen(wp, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout_value, stderr_value = wcpp.communicate()
    wcpp.wait()
    return stdout_value, stderr_value

def reporthook(a,b,c): 
    print "% 3.1f%% of %d bytes\r" % (min(100, float(a * b) / c * 100), c),

def pyget(url, file, folder):
     i = url.rfind('/')
     if ( file == None ):
      file = url[i+1:]
     if ( folder != None ):
      if not os.path.isdir(folder):
         os.makedirs(folder)
      urllib.urlretrieve(url, os.path.join(folder,file), reporthook)
     else:
      urllib.urlretrieve(url,file,reporthook)

def getmsysget():
    if not os.path.exists(os.path.join("tools","PortableGit-1.7.1-preview20100612")):
     pyget("http://shelnutt2.host56.com/public_html/appinstall/PortableGit-1.7.1-preview20100612.zip.exe",None,"tools")
     verifysha1(os.path.join("tools","PortableGit-1.7.1-preview20100612.zip.exe"),"5271f0b1eee46cb39a551c6701fe38572b1acf8c")
     winerun(os.path.join("tools","PortableGit-1.7.1-preview20100612.zip.exe"))
     for file in os.listdir("PortableGit-1.7.1-preview20100612"):
      shutil.move(os.path.join("PortableGit-1.7.1-preview20100612",file),os.path.join("tools","PortableGit-1.7.1-preview20100612"))
     shutil.rmtree("PortableGit-1.7.1-preview20100612")

def filehippo(option,package):
    fh=os.path.join("tools","GetUpdatesFromFilehippo.sh")
    fh= "./" + fh + " " + option + " " + package
    fhp=subprocess.Popen(fh, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout_value, stderr_value = fhp.communicate()
    fhp.wait()
    if stderr_value:
       print (stderr_value)
       reports(package, "FIlehippo: Failed")
    else:
       reports(package, "Filehippo: Success")
    return stderr_value

def testinstall(package):
    ti = os.path.join("tools","autohotkey.exe") + " " + os.path.join("scripts","sha1sums",package + "-sha1sum.ahk")
    tip=winerun(ti)
    return tip[0],tip[1]

def wpkg(package):
    xmldoc = minidom.parse(os.path.join("packages", package + ".xml"))
    reflist = xmldoc.getElementsByTagName('install')      
    bitref = reflist[0]
    a = bitref.attributes["cmd"]
    b = a.value.replace("%SOFTWARE%",SOFTWARE)
    wr=winerun(b)
    tir=testinstall(package)
    
    if any( [repr(wr[1]).find("err:") != -1, repr(wr[1]).find("error") != -1] ):
       reports(package,"Installation: Partial")
    if any( [repr(tir[1]).find("err:") != -1, repr(tir[1]).find("error") != -1] ):
       reports(package,"Installation: Failed")
    else:
       reports(package,"Installation: Success")
    return
    
def testpackage(package):
    tp= os.path.join("tools","autohotkey.exe") + " " + os.path.join("scripts","tests",package + "-tests.ahk")
    tpp=winerun(tp)
    if any( [repr(tpp[1]).find("err:") !=-1, repr(tpp[1]).find("error") !=-1] ):
       reports(package,"Tests: Failed")
    else:
       reports(package,"Tests: Success")
    return tpp[0],tpp[1]


if options.LIST:
   if not os.path.isfile(os.path.join("tools","list")):
      pyget("http://github.com/Shelnutt2/apptester/raw/master/tools/list","list","tools")
   LISTFILE = open(os.path.join("tools","list"), 'r')
   for line in LISTFILE:
	print line,
   LISTFILE.close()
   sys.exit(0)

if 'options.logfilename' in globals():
   pass
else:
   options.logfilename = os.path.join( tempfile.gettempdir(), "apptester.log" ) 
if options.debug:
 if os.path.isfile( options.logfilename ):
   os.remove(options.logfilename)

if options.debug == 0:
  os.environ.__setitem__("WINEDEBUG", 'WINEDEBUG="err,warn-all,fixme-all,trace-all"')

elif options.debug == 1:
  os.environ.__setitem__("WINEDEBUG", 'WINEDEBUG="+trace"')

elif options.debug == 2:
  os.environ.__setitem__("WINEDEBUG", 'WINEDEBUG="+all"')

else:
  sys.exit("Please set a proper debug value")

now = datetime.datetime.now()
HOME=os.environ["HOME"]
os.environ.__setitem__("WINE", "wine")
os.environ.__setitem__("WINECONSOLE", "wineconsole")
os.environ.__setitem__("WINESERVER", "wineserver")
os.environ.__setitem__("WINEPREFIX", os.path.join(HOME, ".wine-appinstall"))
os.environ.__setitem__("APPINSTALL_CACHE", os.path.join(HOME, ".appinstallcache"))
os.environ.__setitem__("TAG", now.strftime("%Y-%m-%d"))

TAG= os.environ["TAG"]
WINE= os.environ["WINE"]
WINECONSOLE= os.environ["WINECONSOLE"]
WINESERVER= os.environ["WINESERVER"]
WINEPREFIX= os.environ["WINEPREFIX"]
APPINSTALL_CACHE= os.environ["APPINSTALL_CACHE"]
SOFTWARE=os.path.join("software")
WINEDEBUG= os.environ["WINEDEBUG"]


if (which(WINE) == None):
    sys.exit("wine not found")

if (which(WINESERVER) == None):
    sys.exit("wineserver not found")

if os.path.isfile(os.path.join("tools","autohotkey.exe")):
    verifysha1(os.path.join("tools","autohotkey.exe"),"7af551a851da5ccb8a98ba980b6b19ec5892884d")


if os.path.isfile(os.path.join("tools","winetricks")):
   os.remove(os.path.join("tools","winetricks")) 
if os.path.exists(WINEPREFIX):
   shutil.rmtree(WINEPREFIX)
pyget("http://winezeug.googlecode.com/svn/trunk/winetricks", os.path.join("tools","winetricks"), None)
cleanup()

if options.All:
   if (which("git") == None):
    getmsysgit()
    if os.path.exists(".git"):
     winerun("tools/PortableGit-1.7.1-preview20100612/bin/git.exe pull")
    else:
     if os.path.exists("tools"):
      shutil.rmtree("tools")
     winerun("tools/PortableGit-1.7.1-preview20100612/bin/git.exe clone https://github.com/Shelnutt2/apptester.git")
     for file in os.listdir("apptester"):
      shutil.move(os.path.join("apptester",file),os.getcwd())

   elif os.path.exists(".git"):
    subprocess.call("git pull", shell=True)

   else:
    if os.path.exists("tools"):
      shutil.rmtree("tools")
    subprocess.call("git clone git://github.com/Shelnutt2/apptester.git", shell=True)
    for file in os.listdir("apptester"):
     shutil.move(os.path.join("apptester",file),os.getcwd())
    shutil.rmtree("apptester")

   if os.path.isfile("autohotkey.exe"):
    verifyahk("autohotkey.exe")

   if not os.path.isfile(os.path.join("tools","list")):
      pyget("http://github.com/Shelnutt2/apptester/raw/master/tools/list","list","tools")
   LISTFILE = open(os.path.join("tools","list"), 'r')
   for line in LISTFILE:
      packdetail= line.strip()
      packdetail= packdetail.translate(None, ' ')
      packdetail= packdetail.split(",")
      if( packdetail[1] == "filehippo" ):
         print "Downloading from filehippo"
         filehippo("download",packdetail[0])
      elif( packdetail[1] == "download.com" ):
         print "need to make download.com script"
      else:
         pyget(packdetail[1], None, os.path.join(SOFTWARE,packdetail[0]))
      if os.listdir(os.path.join(SOFTWARE,packdetail[0])):
         prep_prefix()
         wpkg(packdetail[0])
         testpackage(packdetail[0])
   LISTFILE.close()


wns = WINESERVER + " -k"
wnsp = subprocess.Popen(wns, shell=True)
