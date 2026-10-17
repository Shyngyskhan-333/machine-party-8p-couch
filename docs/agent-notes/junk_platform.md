# junk_platform (8P) - status: done (unverified at runtime)
File: overlay/minigames/junk_platform/scripts/junk_platform.gd
- spawn_players: 4 markers sit on the 4 platform centres (deck radius 6). Extra slots are clones of the transforms shifted +/-2.0 along local X (same facing, so local-mode camera rotation per player is unchanged). Positions are still shuffled in local game.
- junk_handler.max_junk raised to 10*players (80 at 8) when >4 players, since each player spawns junk each tick.
- Elimination/win (active_players.size()>1, scores by death order, winner = player_count) is count-agnostic. Platform collapse is junk-count based, independent of players. No spawn_limit in tscn.
- Unverified: two players per deck 2.0 apart; ref used 1.2.
