#!/usr/bin/python

'''
safari_citrix_settings.py

Purpose:
    ensure .ica is in (Safari) com.apple.DownloadAssessment download Safe category extensions,
    ensure .ica is not in (Safari) com.apple.DownloadAssessment other category extensions
    ensure Open safe downloads is enabled in com.apple.Safari (as is default)
    ensure Citrix Workspace autoupdate is disabled


How:
    Must run in user context, with user logged in at console.
    Uses CoreFoundation PyObjC CoreFoundation to support cached prefs and to avoid need for app restart
    Does not lock down settings like a configuration profile would, suitable for e.g. run-once to provide initial settings
    Does not overwrite existing category lists of safe extensions, strives to be omnipotent

Caveats:
    In order to ensure Open Safe Downloads is enabled, this script needs to be run from an
    executable with full disk access because on recent systems Safari prefs are sandboxed
    and SIP is enabled by default.

ToDo:
    No check yet if prefs were actually stored, future changes like sandboxing might cause issue.

Thanks to:
    https://www.blackmanticore.com/1c569206754935dacb0dc6b89ca818b8
    https://gist.github.com/gregneagle/010b369e86410a2f279ff8e980585c68
    https://gist.github.com/gregneagle/01c99322cf985e771827
    https://lapcatsoftware.com/articles/containers.html
'''

# import plistlib
import os.path
import sys
import CoreFoundation
from Foundation import NSMutableArray, NSMutableDictionary, NSHomeDirectory

def setDownloadAssessmentCategory(extension, risk_category):
    risk_categories = { 'LSRiskCategorySafe', 'LSRiskCategoryNeutral', 'LSRiskCategoryUnsafeExecutable', 'LSRiskCategoryMayContainUnsafeExecutable' }
    for arisk_category in risk_categories:
        # read the dict with current category of safe extensions - gets an immutable return object
        cur_risk_category = CoreFoundation.CFPreferencesCopyAppValue( arisk_category, "com.apple.DownloadAssessment")

        if cur_risk_category:
            # copy immutable dict to new mutable one
            my_risk_category = NSMutableDictionary.alloc().initWithDictionary_copyItems_(cur_risk_category, True)
        else:
            # create an empty dict
            my_risk_category = {}

        if 'LSRiskCategoryExtensions' in my_risk_category:
            cur_risk_exts = my_risk_category['LSRiskCategoryExtensions']
            my_risk_category['LSRiskCategoryExtensions'] = NSMutableArray.alloc().initWithArray_(cur_risk_exts)
        else:
            # create an empty array for the extensions
            my_risk_category['LSRiskCategoryExtensions'] = []

        if arisk_category == risk_category:
            if not extension in my_risk_category['LSRiskCategoryExtensions']:
                my_risk_category['LSRiskCategoryExtensions'].append(extension)
                print 'Adding extension "%s" to risk category array "%s" of com.apple.DownloadAssessment' % (extension, risk_category)
            else:
                print 'extension "%s" is already present in risk category array "%s" of com.apple.DownloadAssessment' % (extension, risk_category)
        else:
            # ensure the_extension is NOT in any of the remaining categories
            if extension in my_risk_category['LSRiskCategoryExtensions']:
                my_risk_category['LSRiskCategoryExtensions'].remove(extension)
                print 'Removing extension "%s" from risk category array "%s" of com.apple.DownloadAssessment' % (extension, arisk_category)
            # save the changed preference
        CoreFoundation.CFPreferencesSetAppValue(arisk_category, my_risk_category,  "com.apple.DownloadAssessment")
    CoreFoundation.CFPreferencesAppSynchronize("com.apple.DownloadAssessment")



def main():
    # ensure .ica is in Safari category for Safe download extensions
    setDownloadAssessmentCategory('ica', 'LSRiskCategorySafe')
    # for testing:
    #setDownloadAssessmentCategory('zip', 'LSRiskCategoryNeutral')

    # ensure Citrix Workspace AutoUpdate is set to manual
    cur_citrix_autoupdate = CoreFoundation.CFPreferencesCopyAppValue( "AutoUpdateState", "com.citrix.receiver.nomas" )
    if not cur_citrix_autoupdate == "Manual":
        CoreFoundation.CFPreferencesSetAppValue( "AutoUpdateState", "Manual", "com.citrix.receiver.nomas" )
        print 'Citrix preference com.citrix.receiver.nomas AutoUpdateState set to Manual'
    else:
        print 'Citrix preference com.citrix.receiver.nomas AutoUpdateState already set to Manual'

    # ensure AutoOpenSafeDownloads is on for com.apple.Safari
    # test if Safari version is Sandboxed by checking for container
    # must attempt to write to sandboxed plist to ensure new setting does not end up in old prefs path as ghost plist
    homeDirectory = NSHomeDirectory()
    if os.path.isdir(homeDirectory + "/Library/Containers/com.apple.Safari"):
        app_ID = homeDirectory + "/Library/Containers/com.apple.Safari/Data/Library/Preferences/com.apple.Safari"
        safari_prefs_path = app_ID + ".plist"
        # test if script has access, SIP will limit access to container contents, must run from app with full disk access priviledge
        if os.access(safari_prefs_path, os.W_OK):
            print 'Access OK to sandboxed Safari prefs at' + safari_prefs_path
        else:
            sys.exit('No access to sandboxed Safari prefs at' + safari_prefs_path + ' - bailing out')
    else:
        # must be old version - not sandboxed yet
        app_ID = 'com.apple.Safari'
        safari_prefs_path = homeDirectory + "/Library/Preferences/" + app_ID + ".plist"
    cur_open_safe_downloads = CoreFoundation.CFPreferencesCopyAppValue( "AutoOpenSafeDownloads", app_ID )
    if cur_open_safe_downloads is None:
        print 'Open safe Downloads for Safari prefs key AutoOpenSafeDownloads key is not present in ' + safari_prefs_path + ' - it defaults to True so that''s OK'
    else:
        if not cur_open_safe_downloads:
            print 'Open safe Downloads is not enabled in ' + safari_prefs_path
            CoreFoundation.CFPreferencesSetAppValue( "AutoOpenSafeDownloads", True, app_ID )
            CoreFoundation.CFPreferencesAppSynchronize( app_ID )
            print 'Open safe Downloads is now set to True for Safari in ' + safari_prefs_path
        else:
            print 'Open safe Downloads for Safari already enabled in ' + safari_prefs_path

    sys.exit(0)



if __name__ == '__main__':
    main()
