extends RefCounted

# 8P MOD: helpers for minigames whose levels only ship four spawn markers.
# Usage: const SpawnHelper = preload("res://mod8p/spawn_helper.gd")
# (class_name is not used on purpose: new global classes would need the
# shipped global_script_class_cache, which this overlay does not touch.)

const COLOR_NAMES: Array[String] = ["red", "blue", "green", "yellow", "purple", "orange", "cyan", "pink"]

# Candidate offsets tried, in order, around a base marker. Distances are in
# metres; the first candidate that has floor under it wins.
const OFFSET_RADII: Array[float] = [1.6, 1.1, 2.2, 0.7]

static func _has_floor(from_node: Node3D, world_pos: Vector3) -> bool:
	var space := from_node.get_world_3d().direct_space_state
	var query := PhysicsRayQueryParameters3D.create(world_pos + Vector3.UP * 3.0, world_pos + Vector3.DOWN * 6.0)
	return not space.intersect_ray(query).is_empty()

# Returns an offset position near `base_pos` that has floor beneath it, spread
# around the circle by `index` so extra players do not stack. Falls back to the
# base position when nothing qualifies (the caller still gets a valid point).
static func safe_offset_position(from_node: Node3D, base_pos: Vector3, index: int) -> Vector3:
	for radius in OFFSET_RADII:
		for k in 8:
			var angle := float(index) * PI * 0.5 + float(k) * PI * 0.25
			var candidate := base_pos + Vector3(sin(angle) * radius, 0.0, cos(angle) * radius)
			if _has_floor(from_node, candidate):
				return candidate
	return base_pos

# Grows a Node3D parent's child markers to `target_count` (Marker3D clones of
# the existing ones, offset to safe ground). Returns the full child list.
static func extend_marker_children(parent: Node3D, target_count: int) -> Array[Node3D]:
	var markers: Array[Node3D] = []
	for c in parent.get_children():
		if c is Node3D and not String(c.name).begins_with("Spawn8P_"):
			markers.append(c)
	var existing := markers.size()
	if existing == 0:
		return markers
	var i := existing
	while markers.size() < target_count:
		var base: Node3D = markers[i % existing]
		var already := parent.get_node_or_null("Spawn8P_%d" % i)
		var m: Node3D = already
		if m == null:
			m = Marker3D.new()
			m.name = "Spawn8P_%d" % i
			parent.add_child(m)
			m.global_transform = base.global_transform
			m.global_position = safe_offset_position(parent, base.global_position, i)
		markers.append(m)
		i += 1
	return markers

# Same for an exported Array[Node3D] of spawn nodes (parent hosts the clones).
static func extend_marker_array(markers: Array, parent: Node3D, target_count: int) -> Array:
	var existing := markers.size()
	if existing == 0:
		return markers
	var out: Array = markers.duplicate()
	var i := existing
	while out.size() < target_count:
		var base: Node3D = markers[i % existing]
		var m := Marker3D.new()
		m.name = "Spawn8P_%d" % i
		parent.add_child(m)
		m.global_transform = base.global_transform
		m.global_position = safe_offset_position(parent, base.global_position, i)
		out.append(m)
		i += 1
	return out

# Keeps raising MultiplayerSpawner.spawn_limit under `root` to at least `count`.
static func raise_spawn_limits(root: Node, count: int) -> void:
	for n in root.find_children("*", "MultiplayerSpawner", true, false):
		if n.spawn_limit != 0 and n.spawn_limit < count:
			n.spawn_limit = count
