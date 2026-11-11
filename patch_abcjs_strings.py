#!/usr/bin/env python3
"""Patch abcjs_basic v6.6.4 or v6.7.2 (minified) so guitar TAB honours per-note string marks.

Usage:  python3 patch_abcjs_strings.py abcjs-basic-min.js abcjs-basic-min.patched.js

Every edit is an exact-string replacement; if the file is a different abcjs version
an assertion fails and nothing is written. Load abcjs-string-marks.js after the patched file.
"""
import sys

src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf8").read()
if not any(v in s[:200] for v in ("abcjs_basic v6.6.4", "abcjs_basic v6.7.2")):
    sys.exit("Expected abcjs_basic v6.6.4 or v6.7.2 - these edits are version specific.")

EDITS = [
    # 1. string picker takes an optional forced string (1 = highest string); out-of-range falls back to automatic
    ("function c(e,t){var r;(t.isAltered",
     "function c(e,t,fs){var r;(t.isAltered"),
    ("for(var n=e.stringPitches.length-1;n>=0;n--)if(t.pitch+t.pitchAltered>=e.stringPitches[n])",
     "if(fs){var nn=e.stringPitches.length-fs;if(nn>=0&&nn<e.stringPitches.length){var a0=Math.round(t.pitch+t.pitchAltered-e.stringPitches[nn]);if(a0>=0&&a0<=24)return{num:a0,str:fs-1,note:t,forced:!0}}}"
     "for(var n=e.stringPitches.length-1;n>=0;n--)if(t.pitch+t.pitchAltered>=e.stringPitches[n])"),
    # 2. chord callers pass the mark through
    ("var s=c(e,i);r.push(s)", "var s=c(e,i,t[n].fs);r.push(s)"),
    ("(n=c(this,r))?o.push(n)", "(n=c(this,r,e[0].fs))?o.push(n)"),
    # 3. the same-string collision fix leaves two forced notes alone
    ("if(n.str==a.str){", "if(n.str==a.str&&!(n.forced&&a.forced)){"),
]
for old, new in EDITS:
    assert s.count(old) == 1, ("anchor not found exactly once", old[:60], s.count(old))
    s = s.replace(old, new)
open(dst, "w", encoding="utf8").write(s)
print("patched ->", dst)
