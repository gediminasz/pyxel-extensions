from collections import deque
import importlib
import os

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer


class Reloader:
    def __init__(self, hot_modules, on_reload):
        self.hot_modules = hot_modules
        self.on_reload = on_reload
        self.channel = deque()

    def watch(self):
        observer = Observer()
        handler = ChannelNotifier(self.channel)
        directories = {os.path.dirname(hot_module.__file__) for hot_module in self.hot_modules}
        for directory in directories:
            observer.schedule(handler, directory)
        observer.start()

    def update(self):
        try:
            modified_path = self.channel.popleft()
            modified_module = self.get_module_by_path(modified_path)
            if modified_module:
                self.reload_module(modified_module)
                self.on_reload()
        except IndexError:
            pass

    def get_module_by_path(self, path):
        for hot_module in self.hot_modules:
            if hot_module.__file__ == path:
                return hot_module

    def reload_all(self):
        for hot_module in self.hot_modules:
            self.reload_module(hot_module)
        self.on_reload()

    def reload_module(self, module):
        print(f'Reloading {module}')
        importlib.reload(module)


class ChannelNotifier(FileSystemEventHandler):
    def __init__(self, channel):
        self.channel = channel

    def on_modified(self, event):
        if event.src_path not in self.channel:
            self.channel.append(event.src_path)
