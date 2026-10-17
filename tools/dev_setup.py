"""Regenerate the editable overlay (src/overlay) from YOUR game + this repo's patches.

  python tools/dev_setup.py          # recovers scripts into ./decompiled, writes ./src/overlay

Edit files under src/overlay, then run tools/make_patches.py to write them back to patches/ and new_files/.
"""
import os, shutil, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _paths import *
from install import apply_diff

if not os.path.isdir(DECOMPILED):
    print("Recovering scripts from", GAME_PCK)
    subprocess.run([GDRE, "--headless", f"--recover={GAME_PCK}", f"--output={DECOMPILED}"],
                   check=True, stdout=subprocess.DEVNULL)
shutil.rmtree(OVERLAY, ignore_errors=True)
for root, _, files in os.walk(os.path.join(ROOT, "patches")):
    for f in files:
        rel = os.path.relpath(os.path.join(root, f), os.path.join(ROOT, "patches"))[:-5].replace("\\", "/")
        orig = open(os.path.join(DECOMPILED, rel), "rb").read().decode("utf-8")
        res = apply_diff(orig, open(os.path.join(root, f), "rb").read().decode("utf-8"))
        dst = os.path.join(OVERLAY, rel)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        open(dst, "w", encoding="utf-8", newline="").write(res)
for root, _, files in os.walk(os.path.join(ROOT, "new_files")):
    for f in files:
        rel = os.path.relpath(os.path.join(root, f), os.path.join(ROOT, "new_files")).replace("\\", "/")
        dst = os.path.join(OVERLAY, rel)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy(os.path.join(root, f), dst)
print("overlay ready:", OVERLAY)
