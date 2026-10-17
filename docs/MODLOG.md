# MODLOG — Machine Party 8P local couch

## Recon (2026-10-16)
- Install: C:\games\videogames\Machine_Party (Machine Party.exe 96 MB, Machine Party.pck 635 MB, steam_api64.dll, godotsteam + steam-multiplayer-peer + audio_gate DLLs)
- Engine: Godot 4.5.2, pck format 3 (um scan). Anti-cheat: none. Loaders: none installed.
- Userdata %APPDATA%\Godot\app_userdata\Machine Party: NOT present yet (game never run here?) 
- um 0.2.0 installed via uv tool; PATH needs %USERPROFILE%\.local\bin. PYTHONUTF8=1.
- um kb: no Machine Party note.
- Prior art:
  - Binary1936/machine-party-8p: v2.1.2, 56-file overlay (40 .gd/16 .tscn) patched INTO Machine Party.pck; raises ONLINE (Steam/ENet) cap 4->8. Files: mod/autoloads/globals.gd, mod/minigames/*. Reuse as reference for per-minigame 8P changes; our target is LOCAL couch, so local handler + input mapping differ.
  - Krunk-theduck/MachinePartyModLoader: exe patches pck so mods/ folder loads; re-run after game updates.
- Backup: pending (um backup create --name machine-party-premod) before ANY write to game dir.

## Phase 2 (2026-10-16)
- GDRE v2.7.4 in C:\mods\gdre; recovered with --headless to decompiled/ (371 .gd). Prior-art PITFALLS #2: headless may silently drop scenes -> recheck tscn count / rerun with display if a needed scene is missing.
- INSTALLED GAME = v2.0.0 (autoloads/globals.gd game_version). Binary1936 overlay targets v2.1.2 -> cannot drop in; port by diffing.
- Local lobby: scenes/local_lobby/scripts/local_lobby.gd, const MAX_PLAYERS=4 (line 5), next_player() loops MAX_PLAYERS, join() via MultiplayerInput devices (-1 = keyboard), update_player_manager() keys PlayerManager.player_presences by device id. Scene local_lobby.tscn: 4 hand-built 3D Player1..4 under LobbyPreviewViewport/LobbyViewport/Players + 4 LocalPlayerLobbyControls (exported array). Needs scene surgery for 5-8 (duplicate nodes).
- Other cap: modules/multiplayer/network_manager.gd MAX_PLAYERS=4 (online; leave alone, local only).
- 4-player consumers: autoloads/player_manager.gd, scenes/local_game/script/local_game.gd, scripts/scenes/game/game.gd, modules/minigame/minigame.gd, ~15 minigames/* scripts.

## Decision 2026-10-16 (user: yes to all)
- Backup done: ~/.universal-modder/backups/machine-party-premod/20261016-195510.zip (712 MB). Restore: um backup restore machine-party-premod.
- Port against v2.0.0. Extraction verified complete (no missing res:// refs). 
- Route: gdre_tools --pck-patch (patch files into copy of pck) -> install = replace Machine Party.pck (backup exists). Distribute as patcher + .gd/.tscn only (no retail pck).

## Lobby verified (2026-10-16)
- Test loop: build.py -> dist/test.pck (pck-patch: overlay .gd, excludes <f>.remap/<f>c) ; run_test.ps1 launches exe from Steam dir with --main-pack dist/test.pck --windowed --resolution 1920x1080 --log-file shots/godot.log -- -8pautolobby -8pdebug (retail pck untouched). F8=fill 8 bots, F9=ready all. Args after `--` are user args (OS.get_cmdline_user_args).
- Retail scripts are .gd.remap -> .gdc; overlay must drop both. Autoloads can't be added without project.binary -> hooks live in patched existing scripts (bootstrap.gd, globals.gd).
- Lobby: 8 seats = 4 original (back row) + 4 clones of seats 0-3 (same pose) shifted (-2,0,+4.5) with cloned chairs (chair_003/001/002/007); panels via extra_seat_position in controls script (set_container_position + name selection). Colors: orange/cyan/pink = tinted shipped textures (Globals.modded_suit_tints). Proof: shots/PROOF_lobby_8players.png (F8+F9, countdown 2.47, 8 ticks).
- Known noise: 16 log ERRORs at lobby load from Node.duplicate() of Skeleton3D subtree ("get_node absolute path", "skeleton_updated disconnect") - harmless so far.
- MultiplayerInput: shared actions parked on device 99 (was 8, collides with 9th pad); fixed _delete_actions_for_device prefix bug (dev 1 would erase 10-19).
- NEXT: briefing screen shows only 4 BOT rows; then minigame spawns/camera/elimination.

## Minigame ports + shared screens (2026-10-16)
- 5 subagents ported 15 minigames (notes in src/notes/*.md, overlay in src/overlay/minigames). Shared: spawn helper src/overlay/mod8p/spawn_helper.gd; briefing screen (8 rows, scale .64), score screen (8 containers cloned, 3D), MultiplayerInput debug_devices (initialize() wipes per-device actions; set_ui_action_device calls initialize()).
- Test hooks (user args after --): -8pautolobby, -8pdebug (F8 fill, F9 ready-all), -8pauto (bots auto-ready in briefing), -8pgame=<MinigameIdentifier int>.
- VERIFIED idx1 ExplodingCollarRace (Minefield): 8 distinct bots, 8 colors, briefing->game->session end, 0 SCRIPT ERROR. Proof shots/PROOF_minefield_8players.png.
- Batch test of the other 14: test_all.ps1 -> shots/summary_<idx>.txt + godot_g<idx>.log + g<idx>_t30/45/60.png.
- Risky per agents: burn_recycle (room B), knife_at_the_office (8 subviewports, layers), chisel_gauntlet (45deg desks), manufacture_gun/disco_dodge spawn_limit=4 in tscn (raised at runtime).

## Final (2026-10-16)
- Batch test of 14 more minigames (idx 0,2,3,4,5,7,9,10,11,12,13,14,16,17) with 8 idle bots: all loaded, 0 SCRIPT ERROR / Parse Error in godot_g<idx>.log, 8-seat spawns visible in shots/sheet_t45.png (contact sheet). Idle bots mean elimination/score screens ran but nobody played: balance & feel unverified.
- Packaging: make_dist.py -> dist/MachineParty8P (35 unified diffs vs user's recovered scripts + new_files/mod8p/spawn_helper.gd + install.py + README.md). install.py rebuilt the pck from the diffs, lobby F8/F9 re-verified (shots/installer_lobby.png). `um publish check` PASS: 38 files, 0 failures, 0 warnings.
- Steam folder was never modified; the game is launched with --main-pack. Restore point still available: um backup restore machine-party-premod (not needed).
- Gotchas: (1) retail scripts are .gd.remap+.gdc, overlay must exclude both; (2) MultiplayerInput.initialize() wipes per-device actions and set_ui_action_device() calls it; (3) args after `--` are user args; (4) Node.duplicate() remaps inner node exports in 4.5 but logs Skeleton3D errors; (5) real 8 pads + Steam Input untested here (no pads).
- Deviations: Binary1936 note about GDRE --headless dropping scenes: verified no missing res:// refs. Online cap untouched. F8 is gated by -8pdebug or debug build instead of #if DEBUG.

## Wander test + final fix (2026-10-17)
- Added mod8p/wander_bots.gd (-8pwander): debug bots press random actions outside the lobby. All 15 minigames re-run with wandering bots: 0 SCRIPT ERROR / Parse Error in godot_w<idx>.log; shots show real movement, deaths, scoring, session end.
- Bug found by wander test: forklift_certified crashed the game at death time (`ERROR: Index p_index = 0 is out of bounds` at get_child(0), blood-decal pool empty with 8 players). Fix: guard in spawn_blood_rpc (get_child_count()==0 -> return). Re-run clean through round end. 1 strike only.
- Package rebuilt (make_dist.py now copies dist_extras/{install.py,README.md}); `um publish check`: PASS 39 files, 0 failures, 0 warnings. Installer dry run OK; generated pck/bat removed from dist.
- Still unverified: 8 humans, real pads + Steam Input, balance/perf (knife_at_the_office, burn_recycle room B).

## INSTALLED into main game (2026-10-17, user approved)
- C:\games\videogames\Machine_Party\Machine Party.pck = patched build (634961892 B, built by dist/MachineParty8P/install.py). Original kept as "Machine Party.pck.vanilla" (634784756 B). Also um backup machine-party-premod.
- Verified: exe launched with no --main-pack, lobby F8/F9 -> 8 bots, countdown, 0 SCRIPT ERROR (shots/installed_lobby.png, godot_installed.log).
- Uninstall: delete patched pck, rename .vanilla back to "Machine Party.pck" (or Steam "Verify integrity"). A Steam game update overwrites the pck and removes the mod.
- Plain launch needs no args; F8/F9 debug only with `-- -8pdebug` launch option (Steam > Properties > Launch Options: `-- -8pdebug`).
