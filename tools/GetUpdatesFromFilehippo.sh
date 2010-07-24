#!/bin/bash

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

# This script checks for the new versions of a package from filehippo.com
# NOTE: If you call this for multiple packages, PLEASE put a delay (5-10 seconds)
# between each call so that you don't over-stress the server!

if [ -z "$1" ]; then
  echo "Downloads the latest version of a package from filehippo.com."
  echo
  echo "Usage: $0 [update/download] <package name>"
  echo
  echo "  where <package name> is the name of the filehippo.com package."
  echo
  echo "Example, URL for Mozilla Firefox is http://www.filehippo.com/download_firefox/"
  echo "so package name is part of the URL after \"download_\", or \"firefox\"."
  exit 1
fi

PACKAGE=$2
BASEURL=http://www.filehippo.com
URL=$BASEURL/download_$PACKAGE
TEMPFILE1=/tmp/$PACKAGE-1.html
TEMPFILE2=/tmp/$PACKAGE-2.html
TEMPFILE3=/tmp/$PACKAGE-3.html
TEMPLOG=/tmp/$PACKAGE.log
EXEDIR="software/$PACKAGE"
XMLDIR="packages"
UNZIPDIR="c:/Program Files/$PACKAGE/"
WGET="wget"
AWK="awk"
UNZIP="unzip"
VERION=$(grep revision $XMLDIR/$PACKAGE.xml | $AWK 'BEGIN { FS="=" } { print $2 }')

if [ ! -d "$EXEDIR" ]; then
    mkdir -p $EXEDIR
fi


if [ ! -d "$XMLDIR" ]; then
    mkdir -p $XMLDIR
fi

#if [ ! -d "$UNZIPDIR" ]; then
#    mkdir -p $UNZIPDIR
#fi



AGENT="Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US; rv:1.9.2.3) Gecko/20100401 Firefox/3.6.3"
WGETOPTIONS="-t 0 -T 300"


$WGET $WGETOPTIONS -U "$AGENT" -q -O $TEMPFILE1 --header="Cookie: Filter=NOBETA=1&NODEMO=0" $URL

if [ `echo $1 | tr [:upper:] [:lower:]` = `echo "update" | tr [:upper:] [:lower:]` ]
 then
echo "Checking for update"
NEWVERSION=$(grep "<h1>" $TEMPFILE1 | $AWK 'BEGIN { FS=">" } { print $2 }' | $AWK 'BEGIN { FS="<" } { print $1 }')
NEWREVISION=$(grep "<h1>" $TEMPFILE1 | $AWK 'BEGIN { FS=">" } { print $2 }' | $AWK 'BEGIN { FS="<" } { print $1 }' |  tr -cd '[[:digit:]]' )

DOWNLOADURL1=$BASEURL`grep "<b>Download<br/>Latest Version</b>" $TEMPFILE1 | $AWK 'BEGIN { FS="\"" } { print $2 }'`

# delay so don't overload the server.
sleep 1

$WGET $WGETOPTIONS -U "$AGENT" -q -O $TEMPFILE2 --header="Cookie: Filter=NOBETA=1&NODEMO=0" $DOWNLOADURL1
DOWNLOADURL2=$BASEURL`grep "Refresh" $TEMPFILE2 | $AWK 'BEGIN { FS="=" } { print $4 }' | $AWK 'BEGIN { FS="\"" } { print $1 }'`


# if the file to download already exists, we are done.

if [ -f $XMLDIR/$PACKAGE.xml ]; then
CURRENTREVISION=$(grep "revision" $XMLDIR/$PACKAGE.xml | $AWK ' BEGIN { FS="\"" } { print $2 }' )
VERSION=$(grep "name" $XMLDIR/$PACKAGE.xml | $AWK ' BEGIN { FS="\"" } { print $2 }')
else
CURRENTREVISION=0
fi
  echo Current revision = $CURRENTREVISION
  echo New revision = $NEWREVISION

if (( $NEWREVISION > $CURRENTREVISION )); then
  echo Current version = $VERSION
  echo New Version = $NEWVERSION

  echo "New version available... downloading..."
  cd $EXEDIR && $WGET $WGETOPTIONS -U "$AGENT" $DOWNLOADURL2 -o $TEMPLOG && cd ../..
FILENAME=$(grep "Saving to:" $TEMPLOG | $AWK 'BEGIN { FS="`" } { print $2 }' | $AWK 'BEGIN { FS="\47" } { print $1 }')



  # create a new package.xml file, but use old silent install commands if old version exists.

if [ -f $XMLDIR/$PACKAGE.xml ]; then
OLDFILENAME=$(grep -m 1 "install" $XMLDIR/$PACKAGE.xml | $AWK ' BEGIN { FS="%SOFTWARE%" } { print $2 }' | $AWK ' BEGIN { FS="\\" } { print $3 }' | $AWK ' BEGIN { FS="\"" } { print $1 }')
INSTALL=$(grep -m 1 "install" $XMLDIR/$PACKAGE.xml | sed s/"$OLDFILENAME"/"$FILENAME"/1)
UPGRADE=$(echo $INSTALL | sed "0,/"install"/s//"upgrade"/")
	
	if [[ -f $EXEDIR/$OLDFILENAME ]]
	then
	echo "Removing old install file"
	rm $EXEDIR/"$OLDFILENAME"
	fi

else
	if [[ "$FILENAME" == *".msi" ]]; then
	INSTALL="<install cmd='msiexec /i /qn \"%SOFTWARE%\\$PACKAGE\\$FILENAME\"' />"
	UPGRADE="<upgrade cmd='msiexec /i /qn \"%SOFTWARE%\\$PACKAGE\\$FILENAME\"' />"

	else 	if [[ "$FILENAME" == *".zip" ]]; then
		INSTALL="<install cmd='$UNZIP \"%SOFTWARE%\\$PACKAGE\\$FILENAME\" -d \"$UNZIPDIR\"' />"
		UPGRADE="<upgrade cmd='$UNZIP \"%SOFTWARE%\\$PACKAGE\\$FILENAME\" -d \"$UNZIPDIR\"' />"

		else
		INSTALL="<install cmd='\"%SOFTWARE%\\$PACKAGE\\$FILENAME\" -ms -s -silent /s /S /Silent /silent /VERYSILENT /SILENT' />"
		UPGRADE="<upgrade cmd='\"%SOFTWARE%\\$PACKAGE\\$FILENAME\" -ms -s -silent /s /S /Silent /silent /VERYSILENT /SILENT' />"
			
		
		fi
	fi

fi

echo  "<?xml version=\"1.0\" encoding=\"UTF-8\"?>

<packages>

<package
   id=\"$PACKAGE\"
   name=\"$NEWVERSION\"
   revision=\"$NEWREVISION\"
   reboot=\"false\"
   priority=\"10\">

   $INSTALL

   $UPGRADE

</package>

</packages>
" > $XMLDIR/$PACKAGE.xml
else
  echo "The $VERSION is still the newest version out there."

fi

fi

if [ `echo $1 | tr [:upper:] [:lower:]` = `echo "download" | tr [:upper:] [:lower:]` ]
 then
  OLDFILENAME=$(grep -m 1 "install" $XMLDIR/$PACKAGE.xml | $AWK ' BEGIN { FS="%SOFTWARE%" } { print $2 }' | $AWK ' BEGIN { FS="\\" } { print $3 }' | $AWK ' BEGIN { FS="\"" } { print $1 }')
  echo "Checking if installer exists"
  if [ ! -f "$EXEDIR/$OLDFILENAME" ]; then
	echo "Installer does not exists, downloading now..."
LATEST=$(grep "<title>" $TEMPFILE1 | grep "Download Firefox 3.6.8" )
    if [ -n "$LATEST" ]; then
         DOWNLOADURL2=$BASEURL`grep "<b>Download<br/>Latest Version</b>" $TEMPFILE1 | $AWK 'BEGIN { FS="\"" } { print $2 }'`

    else
        VERSION=$(grep "name" $XMLDIR/$PACKAGE.xml | $AWK ' BEGIN { FS="\"" } { print $2 }')
        DOWNLOADURL1=$BASEURL`grep "$VERSION" $TEMPFILE1 | $AWK 'BEGIN { FS="\"" } { print $2 }'`

        $WGET $WGETOPTIONS -U "$AGENT" -q -O $TEMPFILE2 --header="Cookie: Filter=NOBETA=1&NODEMO=0" $DOWNLOADURL1
        DOWNLOADURL2=$BASEURL`grep "<b>Download<br/>This Version</b>" $TEMPFILE2 | $AWK 'BEGIN { FS="\"" } { print $2 }'`
fi
        $WGET $WGETOPTIONS -U "$AGENT" -q -O $TEMPFILE3 --header="Cookie: Filter=NOBETA=1&NODEMO=0" $DOWNLOADURL2
        DOWNLOADURL3=$BASEURL`grep "Refresh" $TEMPFILE3 | $AWK 'BEGIN { FS="=" } { print $4 }' | $AWK 'BEGIN { FS="\"" } { print $1 }'`
	cd $EXEDIR && $WGET $WGETOPTIONS -U "$AGENT" -o $TEMPLOG $DOWNLOADURL3 && cd ../..
  fi
fi

# clean up temp files
rm -f $TEMPFILE1
rm -f $TEMPFILE2
rm -f $TEMPFILE3
rm -f $TEMPLOG

# delay so back-to-back calls of thie script don't overload the server.
sleep 1

exit 0
