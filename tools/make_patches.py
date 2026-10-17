"""Write src/overlay back to patches/ (unified diffs vs recovered scripts) and new_files/."""
import os, shutil, difflib, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _paths import *

for sub in ("patches", "new_files"):
    shutil.rmtree(os.path.join(ROOT, sub), ignore_errors=True)
    os.makedirs(os.path.join(ROOT, sub))
patched = new = 0
for root, _, files in os.walk(OVERLAY):
    for f in files:
        rel = os.path.relpath(os.path.join(root, f), OVERLAY).replace("\\", "/")
        dec = os.path.join(DECOMPILED, rel)
        if os.path.exists(dec):
            a = open(dec, "rb").read().decode("utf-8").splitlines(keepends=True)
            b = open(os.path.join(root, f), "rb").read().decode("utf-8").splitlines(keepends=True)
            d = list(difflib.unified_diff(a, b, "a/" + rel, "b/" + rel, n=3))
            if d:
                p = os.path.join(ROOT, "patches", rel + ".diff")
                os.makedirs(os.path.dirname(p), exist_ok=True)
                open(p, "w", encoding="utf-8", newline="").write("".join(d)); patched += 1
        else:
            p = os.path.join(ROOT, "new_files", rel)
            os.makedirs(os.path.dirname(p), exist_ok=True)
            shutil.copy(os.path.join(root, f), p); new += 1
print(patched, "patched,", new, "new")
