# forklift_certified (8P local) - status: done via runtime clone (unverified in-game)
Files: src/overlay/minigames/forklift_certified/scripts/forklift_certified.gd, crate_manager.gd (ported from ref-8p, local-mode adapted: audit/trace code dropped, all else kept).
- Problem: 4 DropAreas (delivery zones, one per player) + 4 spawn markers, paired by the same index; player 5 overran the arrays. Also crate_manager's Poisson sampler loops forever for >=12 crates (roster*2 at 6+ players).
- Fix: at roster > 4, `_mod_expand_yard()` (called first in spawn_players) duplicates 4 zones at the mid-edges of the 2x2 grid (with @export node rebinding, plates lifted above floor, extra grid-plate decal), appends 4 matching markers, registers new zones in delivery_areas + signal. crate_manager gets `mod_set_spawn_region` (free centre cell) and target crates capped at 10 with a 200-attempt bound (also protects 5 players).
- Uses a `zz_mod_add_delivery_areas_rpc` (authority, call_local). Offline peer is authority so it runs locally; if it errors in local mode, change it to a direct call.
- At roster <= 4 nothing runs (vanilla). At 5-7 only some of the 8 zones get an owner; unowned stay black/inactive.
- Unverified: visuals of the added zones (art copied by script) and vehicle collisions in the tighter ring; crate density with 10 crates for 8 players.
- Elimination/ranking logic is generic (dicts keyed by id), no change.
