# spine_breaker (8P) - status: done (unverified at runtime)
File: overlay/minigames/spine_breaker/scripts/spine_breaker.gd
- Only cap was 4 spawn markers. spawn_players builds extra slots for players 5-8: offset 0.9-2.6m from a base marker, requiring floor underneath and a clear horizontal ray from the base marker (local implementation, not SpawnHelper, to add the wall check). Same rotation as the base marker.
- Pace scaling (ported from ref): fuse (device.activation_duration, learned at _ready) and dead time between victims scaled by 3/(players-1), clamped to 1.0, so 1-4 player games are identical and 8-player rounds stay ~75s instead of ~170s. Remove _mod_pace_factor use if full-length rounds are wanted.
- Target choice (pick_random of active_players), end check, scoring are count-agnostic. No spawn_limit in tscn.
- Unverified: extra spawns may still land awkwardly; fallback is the base marker position (stacked).
