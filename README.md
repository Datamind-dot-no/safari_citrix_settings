# safari_citrix_settings
Get Safari to work better with a Citrix and TGX portals, and open Citrix application shortcuts (.ica) open in Citrix Workspace automatically.

## Purpose:
* ensure .ica and .tgx are in (Safari) com.apple.DownloadAssessment download Safe category extensions,
* ensure .ica and .tgx are in (Safari) com.apple.DownloadAssessment other category extensions
* ensure Open safe downloads is enabled in com.apple.Safari (as is default)
* ensure Citrix Workspace autoupdate is disabled


## How:
* Must run in user context, with user logged in at console.
* Uses CoreFoundation PyObjC CoreFoundation to support cached prefs and to avoid need for app restart
* Does not lock down settings like a configuration profile would, suitable for e.g. run-once to provide initial settings
* Does not overwrite existing category lists of safe extensions, strives to be omnipotent
* pkg is built using munkipkg which installs main script (safari_citrix_settings.py) in /Library/Management/
* run the content of munki_postinstall.sh from your software management solution to call the main script with full disk access permission, tested with VMWAre Workspace ONE

## Dependencies
* [MacAdmins Python Recommended](https://github.com/macadmins/python.git) (uses PyObjc CoreFoundation)

## Caveats:
* In order to ensure Open Safe Downloads is enabled, this script needs to be run from an executable with full disk access because on recent systems Safari prefs are sandboxed and SIP is enabled by default.

## ToDo:
- [x] tested on macOS v10.13 - v11.4 running the Python 2 version macOS shipped with
- [x] update to run on Python3 (MacAdmins/python recommended)
- [ ] check if prefs were actually stored, future changes like sandboxing might cause issue.

## Thanks to:
https://www.blackmanticore.com/1c569206754935dacb0dc6b89ca818b8
https://gist.github.com/gregneagle/010b369e86410a2f279ff8e980585c68
https://gist.github.com/gregneagle/01c99322cf985e771827
https://lapcatsoftware.com/articles/containers.html


## Testing / Troubleshooting:
* Forget installed package
> sudo pkgutil --forget no.datamind.munki.pkg.safari_citrix_settings
* check if sandboxed Safari pref for open safe downloads was applied
> defaults read ~/Library/Containers/com.apple.Safari/Data/Library/Preferences/com.apple.Safari.plist AutoOpenSafeDownloads
