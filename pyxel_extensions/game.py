import pyxel

from .reloader import Reloader
from .store import Store
from .selectors import get_scene


class Game:
    def __init__(self, initial_state, initial_scene, hot_modules=()):
        self.init_pyxel()

        initial_state = {
            '__pyxel_extensions__': {
                'scene': initial_scene.get_name()
            },
            **initial_state
        }
        self.store = Store(initial_state)

        self.scene = self.refresh_scene()
        self.store.subscribe(self.change_scene)

        self.reloader = Reloader(hot_modules)

    def init_pyxel(self):
        pyxel.init(160, 120)

    def run(self):
        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_F1):
            self.reloader.reload()
            self.scene = self.refresh_scene()

        self.scene.update()

    def draw(self):
        pyxel.cls(0)
        self.scene.draw()

    def change_scene(self, old_state, new_state):
        if get_scene(new_state) != get_scene(old_state):
            self.scene = self.build_scene(get_scene(new_state))

    def refresh_scene(self):
        return self.build_scene(get_scene(self.store.state))

    def build_scene(self, name):
        return self.scenes_map[name](self.store)

    @property
    def scenes_map(self):
        return {scene.get_name(): scene for scene in self.get_scenes()}

    def get_scenes(self):
        """Must return an iterable of scene classes."""
        raise NotImplementedError
