# disco_dodge (8P port) - status: done (unverified in game)
File: overlay/minigames/disco_dodge/scrips/disco_dodge.gd
- Scene ships 4 markers on tiles (+-2,+-2) and PlayerSpawner.spawn_limit=4 (tscn NOT edited): SpawnHelper.raise_spawn_limits(self, 8) in _ready.
- _mod_extend_markers adds 4 markers at tile centres (+-6, +-2) before spawn_players (SpawnHelper's floor raycast cannot be used: tiles spawn after players). Spawn list is shuffled as before.
- Scoring/elimination use player_count and dictionaries; already N-agnostic. Lead: if spawn_limit still blocks (clients), set spawn_limit=8 in the tscn.
