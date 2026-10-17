# train_race (8P) - status: done
File: overlay/minigames/train_race/scripts/train_race.gd
- Level already has 8 nooks (Left/1-4, Right/5-8) and nook_handler has no hardcoded count; cycle opens max(count+2-rounds,1) nooks, clamps to 8 (first ~3 cycles at 8P eliminate nobody; then tightens by one per cycle). No change needed.
- Only fix: spawn markers (4 shipped). spawn_players() now builds positions: 4 shipped + 4 more 1.2m inboard in x (same z), as in the ref mod, shuffled. Did not use SpawnHelper (ref's offsets are known-good for this tunnel; helper floor-ray radius could put players on the tracks).
- No spawn_limit in the tscn for this minigame. Scoring/dead_players arrays are size-agnostic.
- Unverified: new spawn spots collide-free (ref used identical offsets online).
