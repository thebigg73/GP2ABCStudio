This web app can be used to convert gp (guitar pro) files to abc notation.  OpenSongApp ties in to this web app to allow the feature directly in the app.

It also generates abc with string decorations to allow string numbering for notes in the guitar tab.  
This is done by patching abcjs-basic-min.js using the included python script and the most up to date version from the offical abcjs repository

python3 patch_abcjs_strings.py abcjs-basic-min.js abcjs-basic-min.patched.js
