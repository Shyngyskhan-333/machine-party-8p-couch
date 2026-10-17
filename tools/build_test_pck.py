"""Build a test pck from src/overlay (patched copy of the retail pck). Usage: python tools/build_test_pck.py [out.pck] [--core]
Run the game with:  "Machine Party.exe" --main-pack <out.pck> --windowed --resolution 1920x1080 -- -8pautolobby -8pdebug"""
import os, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _paths import *
OUT = next((a for a in sys.argv[1:] if not a.startswith("--")), os.path.join(ROOT, "dist", "test.pck"))
os.makedirs(os.path.dirname(OUT), exist_ok=True)
CORE = "--core" in sys.argv
CORE_OK = ("mod8p/", "autoloads/", "addons/", "scenes/", "scripts/", "modules/", "minigames/intermission_new/", "minigames/shared/")
args = [GDRE, "--headless", f"--pck-patch={GAME_PCK}", f"--output={OUT}"]
for root, _, files in os.walk(OVERLAY):
    for f in files:
        full = os.path.join(root, f)
        rel = os.path.relpath(full, OVERLAY).replace("\\", "/")
        if rel == "project.godot" or (CORE and not rel.startswith(CORE_OK)):
            continue
        args.append(f"--patch-file={full}=res://{rel}")
        if rel.endswith(".gd"):
            args += [f"--exclude=res://{rel}.remap", f"--exclude=res://{rel}c"]
        elif rel.endswith(".tscn"):
            args += [f"--exclude=res://{rel}.remap"]
sys.exit(subprocess.run(args).returncode)
