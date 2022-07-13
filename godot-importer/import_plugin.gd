
tool
extends EditorImportPlugin


func get_importer_name():
    return "godot-bss-importer"


func get_visible_name():
    return "Scene"


func get_recognized_extensions():
    return ["bss"]


func get_save_extension():
    return "tscn"


func get_resource_type():
    return "PackedScene"


func get_preset_count():
    return 0


func get_import_options(preset):
    return [
        {name="sheet_image", default_value="", property_hint=PROPERTY_HINT_FILE, hint_string="*.png", tooltip="Absolute path to the spritesheet .png."},
    ]


func get_option_visibility(option, options):
    return true


func import(source_file, save_path, options, platform_variants, gen_files):
    var file := File.new()
    var err := file.open(source_file, File.READ)
    if err != OK:
        printerr("Failed to open file: ", err)
        return FAILED

    var content = file.get_as_text()
    var data = parse_json(content)
    file.close()

    var framerate = data["frameRate"]
    var time_offset = 1 / framerate

    var texture = load(options["sheet_image"])
    if not texture:
        return FAILED

    var packed_scene = PackedScene.new()
    var scene = Node2D.new()

    var sprite = Sprite.new()
    scene.add_child(sprite, true)
    sprite.set_owner(scene)

    sprite.set_texture(texture)
    sprite.set_hframes(texture.get_width() / data["tileWidth"])
    sprite.set_vframes(texture.get_height() / data["tileHeight"])
    
    var player = AnimationPlayer.new()
    scene.add_child(player, true)
    player.set_owner(scene)
    
    var count = 0
    for anim_data in data["animations"]:
        var animation = Animation.new()
        var track_index = animation.add_track(Animation.TYPE_VALUE)
        animation.track_set_path(track_index, "./Sprite:frame")

        var time = 0.0
        for i in range(count, anim_data["end"]):
            animation.track_insert_key(track_index, time, i)
            time += time_offset
    
            player.add_animation(anim_data["name"], animation)

        animation.set_length(time)
        count += anim_data["end"]
        
    err = packed_scene.pack(scene)
    if err != OK:
        printerr("Failed to pack scene: ", err)
        return FAILED

    scene.call_deferred('free')

    var filename = save_path + "." + get_save_extension()
    err = ResourceSaver.save(filename, packed_scene)
    if err != OK:
        printerr("Failed to save resource: ", err)
        return FAILED
    
    return OK