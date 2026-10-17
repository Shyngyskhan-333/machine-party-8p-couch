# manufacture_gun (done, unverified)
File: overlay/minigames/manufacture_gun/scripts/manufacture_gun.gd (adapted from ref, online-only disconnect guards dropped)
- Runtime-built markers for roster>4: $SpawnPositions and $WorkstationSpawns grown from 4 to 8 at mid-edges of the rectangle (desks against +-Z walls rotated/slid, see comments).
- remove_empty_workstation_rpc: bounds guard (empty_desk_array has 4 entries; index>=4 would crash).
- spawn_items: 2 items per marker at 5-8 players, offset 1.1u.
- Recipe preview node raised at >4 (zz_mod_raise_item_preview_rpc, works with offline peer call_local) because desk MOD8 covers it.
- MultiplayerSpawner spawn_limit = 4 on PlayerSpawner in manufacture_gun.tscn (line ~2446): raised at runtime to roster size in _mod_expand_for_roster (property write). LEAD: if the game still refuses the 5th spawn, edit the .tscn value to 8 (or 0).
Unverified: whole thing was never run in local mode; the ref is online-tested only.
