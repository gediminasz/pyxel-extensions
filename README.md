# Pyxel Extensions

A collection of helpers for building games with [Pyxel](https://github.com/kitao/pyxel). A framework, if you will.

## Installation

```
pipenv install -e git+https://github.com/gediminasz/pyxel-extensions.git@v0.0.2#egg=pyxel_extensions
```

## Features

* Redux inspired store for game state
* Scenes
* Hot module reloading

## Example

```py
import pyxel

from pyxel_extensions import action
from pyxel_extensions.game import Game
from pyxel_extensions.scene import Scene


class Example(Game):
    def get_scenes(self):
        return (ExampleScene,)


class ExampleScene(Scene):
    def update(self):
        if pyxel.btnp(pyxel.KEY_SPACE):
            self.store.dispatch(increment_counter())

    def draw(self):
        pyxel.text(10, 10, 'Press <space> to increment:', 7)
        pyxel.text(10, 20, str(self.store.state['counter']), 7)


@action
def increment_counter(state):
    return {**state, 'counter': state['counter'] + 1}


if __name__ == '__main__':
    Example(
        initial_state={'counter': 0},
        initial_scene=ExampleScene
    ).run()
```

## See Also

* https://github.com/gediminasz/games
