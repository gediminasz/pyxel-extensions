def change_scene(scene):
    return lambda state: {
        **state,
        '__pyxel_extensions__': {
            **state['__pyxel_extensions__'],
            'scene': scene.get_name()
        }
    }
