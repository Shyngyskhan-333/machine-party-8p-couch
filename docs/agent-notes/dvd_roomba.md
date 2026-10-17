# dvd_roomba (8P local) - status: done (unverified in-game)
File: src/overlay/minigames/dvd_roomba/scripts/dvd_roomba.gd
- spawn_players(): the scene ships 4 Marker3D under PlayerSpawnParent; now `SpawnHelper.extend_marker_children(parent, max(8, roster))` clones markers (Spawn8P_4..7) onto safe floor (raycast) before the shuffle. Without it player 5 indexed past the array.
- Nothing else is per-player indexed: scores/dead_players are dicts keyed by id; end condition `active_players.size() > 1` and score = rank, player_count from roster. Roombas unaffected (own marker set, max_roomba_count unchanged; 8 players share the same hazards -> longer rounds).
- No spawn_limit on the PlayerSpawner in the .tscn (grep found none); no tscn edit needed.
- Unverified: cloned positions are clustered near the shipped markers (offsets 0.7-2.2 m); check no one spawns inside a wall / on top of a roomba start.
