@tool
extends EditorImportPlugin


func _get_importer_name():
    return "godot-bss-importer"


func _get_visible_name():
    return "Scene"


func _get_recognized_extensions():
    return ["bss"]


func _get_save_extension():
    return "tscn"


func _get_resource_type():
    return "PackedScene"


func _get_preset_count():
    return 0


func _get_import_options(path, preset_index):
    return [
        {name="sheet_image", default_value="", property_hint=PROPERTY_HINT_FILE, hint_string="*.png", tooltip="Absolute path to the spritesheet .png."},
    ]

func _get_option_visibility(path, option_name, options):
    return true

func _get_priority():
    return 1.0

func _get_import_order():
    return 0

func _import(source_file, save_path, options, platform_variants, gen_files):
    var file := FileAccess.open(source_file, FileAccess.READ)
    if not file:
        printerr("Failed to open file")
        return FAILED

    var content = file.get_as_text()
    var json = JSON.new()
    var data = json.parse_string(content)
    file.close()

    if not json:
        printerr("Failed to parse file")
        return FAILED

    var framerate = data["frameRate"]
    var time_offset = 1 / framerate

    if options["sheet_image"] == "":
        return OK

    var texture = load(options["sheet_image"])
    if not texture:
        return FAILED

    var packed_scene = PackedScene.new()
    var scene = Node2D.new()

    var sprite = Sprite2D.new()
    scene.add_child(sprite, true)
    sprite.set_owner(scene)

    sprite.set_texture(texture)
    sprite.set_hframes(texture.get_width() / data["tileWidth"])
    sprite.set_vframes(texture.get_height() / data["tileHeight"])

    var player = AnimationPlayer.new()
    scene.add_child(player, true)
    player.set_owner(scene)

    var count = 0
    var animation_library = AnimationLibrary.new()
    for anim_data in data["animations"]:
        var animation = Animation.new()
        var track_index = animation.add_track(Animation.TYPE_VALUE)
        animation.track_set_path(track_index, "./Sprite:frame")

        var time = 0.0
        for i in range(count, anim_data["end"]):
            animation.track_insert_key(track_index, time, i)
            time += time_offset

            animation_library.add_animation(anim_data["name"], animation)

        animation.set_length(time)
        count += anim_data["end"]
    player.add_animation_library("bss", animation_library)

    var err = packed_scene.pack(scene)
    if err != OK:
        printerr("Failed to pack scene: ", err)
        return FAILED

    scene.call_deferred('free')

    var filename = save_path + "." + _get_save_extension()
    err = ResourceSaver.save(packed_scene, filename)
    if err != OK:
        printerr("Failed to save resource: ", err)
        return FAILED

    return OK
