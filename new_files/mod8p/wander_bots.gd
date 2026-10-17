extends Node

# 8P MOD: test aid (-8pwander). Debug bots (device ids 100+) press random
# actions so minigames see movement, kills and scoring instead of idle bots.

const ACTIONS: Array[String] = ["left", "right", "up", "down", "action_1", "action_2"]
const TICK: float = 0.35

var _elapsed: float = 0.0
var _held: Dictionary = {}

func _process(delta: float) -> void:
	_elapsed += delta
	if _elapsed < TICK:
		return
	_elapsed = 0.0
	var scene := get_tree().current_scene
	if scene == null or scene.scene_file_path.contains("local_lobby"):
		return
	for device in MultiplayerInput.debug_devices:
		for a in ACTIONS:
			var name := "%d%s" % [device, a]
			if not InputMap.has_action(name):
				continue
			var want := randf() < (0.5 if a in ["left", "right", "up", "down"] else 0.25)
			var key := name
			if want and not _held.get(key, false):
				Input.action_press(name, randf_range(0.6, 1.0))
				_held[key] = true
			elif not want and _held.get(key, false):
				Input.action_release(name)
				_held[key] = false
