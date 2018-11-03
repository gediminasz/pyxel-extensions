from dataclasses import dataclass

from .store import Store


@dataclass(frozen=True)
class Scene:
    store: Store

    @classmethod
    def get_name(cls):
        return f'{cls.__module__}.{cls.__name__}'
