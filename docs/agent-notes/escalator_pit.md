# escalator_pit (8P port) - status: done (unverified in game)
File: overlay/minigames/escalator_pit/scripts/escalator_pit.gd
- _enter_tree (roster >4): duplicates the 4 Path3D stair lanes, shifts each pair to centre -/+1.6 (8 strips), duplicates the 4 CRT screens, hides "cylinder" dividers and "Plane_003" handrails (adapted from ref mod).
- spawn_players uses _mod_spawn_position(counter): lane x, y=-2, z of shipped marker. Seats 0-3 left strips, 4-7 right strips. No tscn edit; no spawn_limit on this scene.
- Win/elimination logic is already count-agnostic. Unverified: visuals (strips clipping the baked platform), ref also dropped base platform by 0.75 - not ported.
