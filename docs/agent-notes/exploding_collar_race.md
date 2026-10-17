# exploding_collar_race (done, unverified)
File: overlay/minigames/exploding_collar_race/scripts/exploding_collar_race.gd
- spawn_players(): scene ships 4 markers ("player spawn positions/player spawn 0..3"); grown to 8 with SpawnHelper.extend_marker_array (safe-floor offset clones) before the shuffle. Previously player_positions[4] was out of bounds.
- spawn_limit: none set in the .tscn (default 0 = unlimited), nothing to do.
- Camera (z average of active players), scoring, finish/explode logic are dictionary/array based, no 4 assumptions.
Unverified: clone positions are raycast-based; check 8 players do not spawn on mines/overlap at the start line.
