#!/bin/bash

###########################      About this script      ##########################
#                                                                                #
#   safari_citrix_settings.py - (Munki)postinstall script                        #
#                                                                                #
#   Purpose:                                                                     #
#           call safari_citrix_settings.py script as console user                #
#            *** with full disk access ***                                       #
#                                                                                #
#   Created by Martinus Verburg                                                  #
#               March 2021                                                       #
#                                                                                #
#   Changelog                                                                    #
#            2021-06-14 - moved away from munkipkg postinstall as apparently     #
#                         the Installer app doesn't have full disk access while  #
#                         WS1-Munki does run it successfully as                  #
#                         postinstall script in the pkginfo                      #
#                                                                                #
#                                                                                #
#   Instructions                                                                 #
#            designed to run by software management application as console user  #
#            such as VMware Workspace ONE, Munki                                 #
#            MUST be run from process entitled to full disk access in order to   #
#            write to sandboxed Safari settings                                  #
#            in ~/Library/Containers/com.apple.Safari                            #
#                                                                                #
##################################################################################

# Wait until Finder is running to ensure a console user is logged in
while ! pgrep -q Finder ; do
		echo "Waiting until console user is logged in"
		sleep 10
done

# get Console user
# Thanks to Graham Pugh - copied from erase-install.sh
current_user=$(/usr/sbin/scutil <<< "show State:/Users/ConsoleUser" | /usr/bin/awk -F': ' '/[[:space:]]+Name[[:space:]]:/ { if ( $2 != "loginwindow" ) { print $2 }}')

sudo -u $current_user /Library/Management/safari_citrix_settings.py
