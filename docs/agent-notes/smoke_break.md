# smoke_break (8P) - status: done (unverified at runtime)
Files: overlay/minigames/smoke_break/scripts/smoke_break.gd, scripts/smoke_break_trolley.gd, components/player/scripts/smoke_break_player_anim_handler.gd
- smoke_break.gd: in _ready (every peer) when >4 players, adds 4 Marker3D seats (Spawn8P_4..7) under PlayerSpawner/PlayerPositions using seat transforms taken from the ref v2.1.2 scene, and duplicates crate1_003 twice (seats 4 and 7 hang off the bench ends). Extends player_spawn_positions to 8. Seats 0-3 untouched.
- trolley: rot_by_seat_index_array extended to 8 in _ready (aim angles from ref); smoke particle index wrapped (only 4 puffs); blood decal skipped for seats >=4 (only 4 decal nodes; cosmetic).
- anim handler: finish_look + death animations for seats 4-7 (previously "" -> no anim).
- Scoring/end: top 3 finishers +1, losers shot; counts all players already. No spawn_limit in the tscn. Suit colour is set from customization data (lead/globals).
- Unverified: seat positions/crate placement are ref values (not visually checked); camera framing unchanged (ref did not change it).
