"""Machine Party 8-player couch mod - builds MachineParty8P.pck from YOUR copy of the game.

Nothing from the retail game is shipped with this mod. This script:
  1. recovers the scripts from your own `Machine Party.pck` with GDRE Tools (into a temp folder),
  2. applies the bundled patches/ to those scripts and adds new_files/,
  3. writes a patched COPY of the pck next to this script (the Steam folder is NOT modified),
  4. writes Play8P.bat that starts the game with that pck (--main-pack).

Usage:  python install.py --game "C:\\...\\Machine Party" --gdre "C:\\tools\\gdre_tools.exe"
Game version this was built against: v2.0.0 (Godot 4.5.2). Other versions: patches may not apply.
"""
import argparse, os, shutil, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))


def apply_diff(original: str, diff: str) -> str:
    src = original.splitlines(keepends=True)
    out, pos = [], 0
    lines = diff.splitlines(keepends=True)
    i = 0
    while i < len(lines) and not lines[i].startswith("@@"):
        i += 1
    while i < len(lines):
        h = lines[i]
        start = int(h.split()[1].split(",")[0][1:]) - 1
        out += src[pos:start]
        pos = start
        i += 1
        while i < len(lines) and not lines[i].startswith("@@"):
            l = lines[i]
            tag, body = l[0], l[1:]
            if tag == " ":
                if src[pos] != body:
                    raise ValueError("context mismatch (different game version?)")
                out.append(src[pos]); pos += 1
            elif tag == "-":
                if src[pos] != body:
                    raise ValueError("removal mismatch (different game version?)")
                pos += 1
            elif tag == "+":
                out.append(body)
            i += 1
    out += src[pos:]
    return "".join(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", required=True, help="folder containing Machine Party.exe / Machine Party.pck")
    ap.add_argument("--gdre", required=True, help="path to gdre_tools.exe (https://github.com/GDRETools/gdsdecomp)")
    a = ap.parse_args()

    pck = os.path.join(a.game, "Machine Party.pck")
    exe = os.path.join(a.game, "Machine Party.exe")
    if not (os.path.isfile(pck) and os.path.isfile(exe)):
        sys.exit("Machine Party.exe / .pck not found in --game")
    if not os.path.isfile(a.gdre):
        sys.exit("gdre_tools.exe not found")

    work = tempfile.mkdtemp(prefix="mp8p_")
    rec = os.path.join(work, "recovered")
    print("Recovering scripts from your pck (about a minute)...")
    subprocess.run([a.gdre, "--headless", f"--recover={pck}", f"--output={rec}"],
                   check=True, stdout=subprocess.DEVNULL)

    stage = os.path.join(work, "stage")
    cmd = [a.gdre, "--headless", f"--pck-patch={pck}",
           f"--output={os.path.join(HERE, 'MachineParty8P.pck')}"]
    n = 0
    for root, _, files in os.walk(os.path.join(HERE, "patches")):
        for f in files:
            rel = os.path.relpath(os.path.join(root, f), os.path.join(HERE, "patches"))[:-5].replace("\\", "/")
            orig = open(os.path.join(rec, rel), "rb").read().decode("utf-8")
            diff = open(os.path.join(root, f), "rb").read().decode("utf-8")
            res = apply_diff(orig, diff)
            dst = os.path.join(stage, rel)
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            open(dst, "w", encoding="utf-8", newline="").write(res)
            cmd.append(f"--patch-file={dst}=res://{rel}")
            cmd += [f"--exclude=res://{rel}.remap", f"--exclude=res://{rel}c"]
            n += 1
    for root, _, files in os.walk(os.path.join(HERE, "new_files")):
        for f in files:
            full = os.path.join(root, f)
            rel = os.path.relpath(full, os.path.join(HERE, "new_files")).replace("\\", "/")
            cmd.append(f"--patch-file={full}=res://{rel}")
            n += 1
    print(f"Building MachineParty8P.pck ({n} files)...")
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL)
    shutil.rmtree(work, ignore_errors=True)

    bat = os.path.join(HERE, "Play8P.bat")
    open(bat, "w").write(
        f'@echo off\r\ncd /d "{a.game}"\r\n'
        f'start "" "Machine Party.exe" --main-pack "{os.path.join(HERE, "MachineParty8P.pck")}" %*\r\n'
        "rem add  -- -8pdebug  to enable F8 (fill 8 bots) / F9 (ready all) in the lobby\r\n")
    print("Done. Start the game with Play8P.bat (the Steam folder was not modified).")


if __name__ == "__main__":
    main()
