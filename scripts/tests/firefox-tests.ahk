;
; AutoHotKey Test Script for Mozilla Firefox 3.5
;
; Copyright (C) 2009 Austin English
;
; This library is free software; you can redistribute it and/or
; modify it under the terms of the GNU Lesser General Public
; License as published by the Free Software Foundation; either
; version 2.1 of the License, or (at your option) any later version.
;
; This library is distributed in the hope that it will be useful,
; but WITHOUT ANY WARRANTY; without even the implied warranty of
; MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
; Lesser General Public License for more details.
;
; You should have received a copy of the GNU Lesser General Public
; License along with this library; if not, write to the Free Software
; Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301, USA
;

#Include tools/helper_functions
#Include tools/init_test

SetWorkingDir, %A_Programfiles%\Mozilla Firefox

Run, firefox.exe
ERROR_TEST("Running Firefox failed.", "Running Firefox went okay.")

TODO_WINDOW_WAIT("Import Wizard", 19089,"", 5)
IfWinExist, Import Wizard
{
ControlSend, MozillaWindowClass18, {Escape}, Import Wizard
ERROR_TEST("Closing Import Wizard reported an error.", "Closing Import Wizard went fine.")
Sleep 500
WIN_EXIST_TEST("Import Wizard")
}

WINDOW_WAIT("Default Browser")
ControlSend, MozillaWindowClass1, {Enter}, Default Browser
Sleep 500
WIN_EXIST_TEST("Default Browser")
ERROR_TEST("Default Browser reported an error.", "Default Browser closed fine.")

WINDOW_WAIT("Welcome to Firefox - Mozilla Firefox")
ERROR_TEST("Firefox's main window reported an error.", "Firefox appears to be running fine.")

CLOSE("Welcome to Firefox - Mozilla Firefox")
WINDOW_WAIT("Quit Firefox")
ControlSend, MozillaWindowClass1, Q, Quit Firefox
ERROR_TEST("Exiting Firefox gave an error.", "Firefox claimed to exit fine.")
Process, Waitclose, firefox.exe, 10 ; Give firefox up to 10 seconds to close
ERROR_TEST("Exiting Firefox process gave an error.", "Firefox process claimed to exit fine.")
WIN_EXIST_TEST("Quit Firefox")
WIN_EXIST_TEST("Welcome to Firefox - Mozilla Firefox")

; Test for bug 14771
Run, firefox.exe
ERROR_TEST("Running Firefox failed.", "Running Firefox went okay.")

WinWait, Default Browser, , 3
    if ErrorLevel
    {
        FileAppend, Default Browser didn't appear. Bug 14771 TODO_FIXED.`n, %OUTPUT%
    }
    Else
    {
        FileAppend, Default Browser appeared. Bug 14771 TODO_FAILED.`n, %OUTPUT%
        IfWinNotActive, Default Browser
            {
            WinActivate, Default Browser
            }
        ControlSend, MozillaWindowClass1, {Enter}, Default Browser
    }

WINDOW_WAIT("Mozilla Firefox Start Page - Mozilla Firefox")
ERROR_TEST("Firefox's main window reported an error.", "Firefox appears to be running fine.")

CLOSE("Mozilla Firefox Start Page - Mozilla Firefox")
Process, Waitclose, firefox.exe, 10 ; Give firefox up to 10 seconds to close
ERROR_TEST("Exiting Firefox process gave an error.", "Firefox process claimed to exit fine.")
WIN_EXIST_TEST("Mozilla Firefox Start Page - Mozilla Firefox")

; Make sure setting default browser manually works:
Runwait, firefox.exe -silent -setDefaultBrowser
ERROR_TEST("Setting default browser to Firefox failed.", "Setting default browser to Firefox went okay.")
Process, Waitclose, firefox.exe, 10 ; Give firefox up to 10 seconds to close
ERROR_TEST("Exiting Firefox process gave an error.", "Firefox process claimed to exit fine.")
Run, start http://www.google.com/
WinWait, Default Browser, , 3
    if ErrorLevel
    {
        FileAppend, Firefox didn't pop up default browser check. Test passed.`n, %OUTPUT%
    }
    Else
    {
        FileAppend, Firefox default browser check appeared. Test failed.`n, %OUTPUT%
        IfWinNotActive, Default Browser
            {
            WinActivate, Default Browser
            }
        ControlSend, MozillaWindowClass1, {Enter}, Default Browser
    }

WINDOW_WAIT("Google - Mozilla Firefox")
ERROR_TEST("Opening google.com reported an error.", "Opening google.com went okay.")

CLOSE("Google - Mozilla Firefox")
Process, Waitclose, firefox.exe, 10 ; Give firefox up to 10 seconds to close
ERROR_TEST("Exiting Firefox process gave an error.", "Firefox process claimed to exit fine.")
WIN_EXIST_TEST("Google - Mozilla Firefox")

; Make sure bug 19220 doesn't regress:
Run, firefox.exe http://www.mozilla.com/en-US/firefox/3.5b99/whatsnew/
ERROR_TEST("Running firefox what's new failed.", "Running firefox what's new went okay.")
WinWait, Default Browser, , 3
    if ErrorLevel
    {
        FileAppend, Firefox didn't pop up default browser check. Test passed.`n, %OUTPUT%
    }
    Else
    {
        FileAppend, Firefox default browser check appeared. Test failed.`n, %OUTPUT%
        IfWinNotActive, Default Browser
            {
            WinActivate, Default Browser
            }
        ControlSend, MozillaWindowClass1, {Enter}, Default Browser
    }
WINDOW_WAIT("Welcome to Firefox 3.5 Preview - Mozilla Firefox")
ERROR_TEST("Opening what's new page reported an error.", "Opening what's new page went okay.")

CLOSE("Welcome to Firefox 3.5 Preview - Mozilla Firefox")
Sleep 500
WIN_EXIST_TEST("Welcome to Firefox 3.5 Preview - Mozilla Firefox")

TEST_COMPLETED()

exit 0
