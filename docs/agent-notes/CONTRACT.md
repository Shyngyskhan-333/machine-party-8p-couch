# Contract for 8P minigame ports (local couch mode, game v2.0.0)

World: local game = OfflineMultiplayerPeer; every minigame runs as "server" (multiplayer.is_server() true).
Roster: PlayerManager.player_presences : Dictionary[int, PlayerPresence], key = device id
(-1 keyboard, 0..7 pads, 100..107 F8 debug bots). Up to 8 entries, insertion order = seat order.
Suit colors per seat (index 0..7): red, blue, green, yellow, purple, orange, cyan, pink (Globals.suit_colors).

Rules for each patched file:
- Source = C:\mods\machine-party-8p\decompiled\<res path>. Write patched copy to
  C:\mods\machine-party-8p\src\overlay\<same res path>. NEVER edit decompiled/ or the Steam folder.
- Preserve the file's existing indentation (tabs) and line endings. Mark every change with a `# 8P MOD` comment.
- Prefer .gd-only changes. Avoid editing .tscn (huge); if a scene change is unavoidable, do it in script at runtime.
- Use `const SpawnHelper = preload("res://mod8p/spawn_helper.gd")` for spawn markers (see src/overlay/mod8p/spawn_helper.gd).
- Do not touch: autoloads/globals.gd, scenes/local_lobby/*, scenes/local_game/*, scripts/scenes/game/*,
  minigames/intermission_new/*, minigames/shared/*, modules/minigame/* (owned by the lead). If a minigame needs a change there, write it in your note.
- Reference only (do not copy blindly, it targets v2.1.2 and ONLINE mode): C:\mods\machine-party-8p\src\ref-8p\mod\... (MIT). Diff against decompiled to see what changed; v2.0.0 vs v2.1.2 differences are noise.
- Do not run the game. Lead builds & tests. Write a note src/notes/<minigame>.md: files changed, what each change does, anything unverified, anything you could not make work for 8.
Goal per minigame: 8 players spawn at distinct safe positions; every per-player array/dictionary/index/color/camera/teams/win-elimination logic handles 8 (no "index out of bounds", no hardcoded 4/3/range(4)); round end conditions count all 8.
