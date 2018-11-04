from .reducer import action


@action
def change_scene(state, scene):
    return {
        **state,
        '__pyxel_extensions__': {
            **state['__pyxel_extensions__'],
            'scene': scene.get_name()
        }
    }
