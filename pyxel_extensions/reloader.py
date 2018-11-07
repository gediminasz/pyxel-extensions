from queue import Queue, Empty
import importlib
import os

from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler


class Reloader:
    def __init__(self, hot_modules, on_reload):
        self.hot_modules = hot_modules
        self.on_reload = on_reload
        self.channel = Queue()

    def watch(self):
        observer = Observer()
        for hot_module in self.hot_modules:
            path = hot_module.__file__
            handler = FileModifiedHandler(
                on_modified = lambda: self.channel.put(hot_module),
                patterns=(path,)
            )
            observer.schedule(handler, os.path.dirname(path))
        observer.start()

    def update(self):
        try:
            modified_module = self.channel.get_nowait()
            self.reload_module(modified_module)
            self.on_reload()
        except Empty:
            pass

    def reload_all(self):
        for hot_module in self.hot_modules:
            self.reload_module(hot_module)
        self.on_reload()

    def reload_module(self, module):
        print(f'Reloading {module}')
        importlib.reload(module)


class FileModifiedHandler(PatternMatchingEventHandler):
    def __init__(self, on_modified, *args, **kwargs):
        self._on_modified = on_modified
        super().__init__(*args, **kwargs)

    def on_modified(self, event):
        self._on_modified()
