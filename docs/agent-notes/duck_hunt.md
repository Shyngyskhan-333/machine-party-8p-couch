# duck_hunt (8P port) - status: done (unverified in game)
Files: overlay/minigames/duck_hunt/scripts/duck_hunt.gd, .../components/hunter_player/scripts/hunter_player.gd
- Roles: 1 hunter + (N-1) ducks, scales by itself. Blocker was 3 duck spawn markers: _mod_expand_spawn_markers() adds Marker3Ds at half spacing, alternating outward, same z, within FinishArea half width 11.75 (idempotent across Reset turns).
- hunter_player: magazine/reload dicts extended for 4-7 ducks (vanilla fell back to 7 shells). Ref's anim-speed fit not ported: bolt animation may clip at 4+ ducks (cosmetic).
- duck_hunt.gd: removed bogus duck_player_count decrement when hunter leaves; null-guards on hunter_player in _on_player_died.
- Local mode: all ducks share one half-screen camera (average of living ducks); 7 ducks fit, not tested.
- Ref also patched -startgame skip-reveal; not needed in local couch.
