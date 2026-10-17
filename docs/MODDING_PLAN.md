# MODDING_PLAN
Route: Godot playbook route 1 — GDRE recover to C:\mods\machine-party-8p\decompiled (read-only study), ship only own modified .gd/.tscn as overlay pck (no retail assets).
1. Extract pck with GDRE Tools (outside install).
2. Locate: MAX_PLAYERS, color palette, local lobby/join + joypad device mapping, spawner, camera, elimination, lobby layout.
3. Diff against Binary1936 overlay for ideas; write own local-mode patch (src/).
4. Build overlay pck (godot --export-pack or gdre pck tool). Install via overlay loading (res:// override) — ASK before writing to Steam folder.
5. Verify: godot.log, F8 debug fill, screenshots (um win).
6. um publish check dist; README.
Zero fal spend. Offline only. 3-strike breaker active.
