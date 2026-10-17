# Machine Party - 8-Player Couch Mod

Raises **local couch co-op** (offline) from 4 to **8 players** for Machine Party **v2.0.0** (Godot 4.5.2).
Online/Steam multiplayer is not touched. Built with AI assistance (Claude Code) on top of GDRE Tools.
Prior art credited: Binary1936/machine-party-8p (online 8P mod, MIT) was used as a reference for what each minigame needed.

## What changes
- Lobby seats 8 players (two rows), 8 high-contrast suit colours (red, blue, green, yellow, purple, orange, cyan, pink; the last three are tinted shipped textures).
- Briefing and score screens list 8 rows.
- All 15 rotation minigames spawn 8 players with safe spawn offsets, 8-way split screens where needed, and round/elimination logic counting all 8.
- Controller polling uses device ids 0-7; shared actions are parked on device 99.

## Install (no game files are shipped - bring your own copy)
1. Install Python 3 and download GDRE Tools (https://github.com/GDRETools/gdsdecomp/releases, tested with v2.7.4).
2. `python install.py --game "C:\path\to\Machine Party" --gdre "C:\path\to\gdre_tools.exe"`
   This recovers scripts from YOUR pck, applies `patches/`, and writes `MachineParty8P.pck` plus `Play8P.bat` next to the script (about 635 MB). The Steam folder is not modified.
3. Start the game with `Play8P.bat`. Uninstall = delete those two files.

After a game update, patches may no longer apply; re-run the installer (it reports a context mismatch if so).

## Controllers (8 pads on one PC)
- Use Steam Input per controller (Steam > Settings > Controller): enable Xbox/Generic support, give each pad its own player slot. Connect all pads before launching.
- Each player presses a button in the lobby to join; the first joiner is the main player.
- Keyboard counts as one extra device (id -1), so 7 pads + keyboard also works.
- 1920x1080 windowed or fullscreen both fit; the UI scales from the game's 960x540 base.

## Troubleshooting
- A pad does not join: unplug/replug, check it appears in Windows "Set up USB game controllers", and remove duplicate virtual pads from Steam Input.
- Only 4 players in the lobby: you launched the normal exe, use `Play8P.bat`.
- A pad is device 8 or higher: only ids 0-7 are used by the game; fewer virtual pads fixes it.
- Install says "context mismatch": your game is not v2.0.0.
- Lobby shows 16 harmless log errors about Skeleton3D at load (cloned seats).

## Debug (optional)
`Play8P.bat -- -8pdebug`: in the lobby F8 fills the remaining seats with bots, F9 readies everyone. `-8pgame=<id>` plays one minigame; `-8pauto` auto-readies bots; `-8pwander` makes bots walk and act randomly.

## Known limits
- Verified with 8 scripted bots (idle and random-walking), never with 8 humans or real pads: spawns, split screens, briefing/score and round end ran in all 15 minigames without script errors. Balance and feel at 8 are untested; knife_at_the_office and burn_recycle (second room for seats 5-8) are the riskiest. Cap those at 4-6 players if they misbehave.

## Development (continue from a fresh clone)
The repo stores only diffs and new files, never retail code. To get an editable tree:
1. Put GDRE Tools somewhere and set `MP_GDRE` (and `MP_GAME_DIR` if your game is not in the default Steam path); keep an untouched pck (`Machine Party.pck.vanilla` is used automatically if the mod is installed in place).
2. `python tools/dev_setup.py` - recovers scripts into `decompiled/` and writes the patched, editable tree to `src/overlay/` (both git-ignored).
3. Edit `src/overlay/...`. Build a test pck: `python tools/build_test_pck.py` then run it with `tools/run_test.ps1` (launches with `--main-pack`, the Steam pck stays untouched). Per-minigame tests with 8 wandering bots: `tools/test_game.ps1 -Idx <MinigameIdentifier>` (needs [`um`](https://github.com/rehan-remade/universal-modder) for screenshots).
4. `python tools/make_patches.py` writes your edits back to `patches/` and `new_files/`. Commit those.

Test hooks (user args after `--`): `-8pautolobby`, `-8pdebug` (F8 fill / F9 ready), `-8pauto`, `-8pwander`, `-8pgame=<id>`.

Layout: `patches/` diffs - `new_files/` new scripts (`mod8p/`) - `install.py` end-user installer - `tools/` dev scripts - `docs/MODLOG.md` field notes and gotchas - `docs/agent-notes/` per-minigame port notes - `docs/proof/` screenshots.
