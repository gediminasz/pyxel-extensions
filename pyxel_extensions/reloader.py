from dataclasses import dataclass
from types import ModuleType
import importlib
import os


@dataclass
class HotModule:
    module: ModuleType
    last_reloaded_at: float = None

    def __post_init__(self):
        self.last_reloaded_at = self.file_modified_at

    @property
    def is_stale(self):
        return self.file_modified_at > self.last_reloaded_at

    def reload(self):
        print(f'Reloading {self.module}')
        importlib.reload(self.module)
        self.last_reloaded_at = self.file_modified_at

    @property
    def file_modified_at(self):
        return os.path.getmtime(self.module.__file__)


class Reloader:
    def __init__(self, modules):
        self.hot_modules = tuple(HotModule(module=module) for module in modules)

    def reload(self):
        for hot_module in self.hot_modules:
            if hot_module.is_stale:
                hot_module.reload()
