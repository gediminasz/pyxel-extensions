import pyxel

from .reloader import Reloader
from .store import Store


class Game:
    def __init__(self, initial_state, reducer, scenes, hot_modules=()):
        self.init_pyxel()

        self.store = Store(initial_state, reducer)

        self.scenes_map = {scene.name: scene for scene in scenes}

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
            self.scene = self.build_scene(self.store.state['__scene__'])

        self.scene.update()

    def draw(self):
        pyxel.cls(0)
        self.scene.draw()

    def change_scene(self, old_state, new_state):
        if new_state['__scene__'] != old_state['__scene__']:
            self.scene = self.refresh_scene()

    def refresh_scene(self):
        return self.build_scene(self.store.state['__scene__'])

    def build_scene(self, name):
        return self.scenes_map[name](self.store)
