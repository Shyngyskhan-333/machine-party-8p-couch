# chisel_gauntlet_multiplayer (done, unverified)
Files (overlay/minigames/chisel_gauntlet_multiplayer/): scripts/chisel_gauntlet.gd, scripts/chisel_gauntlet_local_handler.gd, components/player/scripts/chisel_gauntlet_player.gd
- player_rotations extended to 8 facings (45 deg steps; extra seats sit between the 4 desks). All players share one spawn point, distinguished only by rotation.
- spectate_positions (4 markers, all at the same point) repeated up to 8 at initialize().
- >4 players: shotgun_check_order = clockwise 8-slot sweep (otherwise seats 5-8 would never be shot); 4 extra desks built at runtime by duplicating the 4 station nodes rotated 45 deg (ported from the ref, plain func, no RPC); barrel_001/002 hidden (clip the 135 deg seat). .tscn untouched.
- Local handler Layouts: added 5/6 (3x2 grid) and 7/8 (4x2 grid) split-screen cells.
- Player setup_local_visuals: vanilla used 2 render layers per player (10+idx*2) which overflows the 20 visual layers at 8. Now 1 bit per player (10..17): own first-person on bit i; third-person meshes/hats on all bits except i; camera i enables bit i. Same visible result as vanilla.
- Not ported: the ref's jumbotron HUD overlay (online only; couch mode already uses its own jumbotron viewport).
- spawn_limit on PlayerSpawner: not set in the .tscn (unlimited).
Unverified: the 4 added desks/camera "look at desk" animations at 45 deg, viewport cell aspect (8p cells are 480x540 portrait at 1080p).
