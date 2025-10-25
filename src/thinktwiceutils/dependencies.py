import hashlib
from collections.abc import Callable
from contextlib import contextmanager
from typing import Any


class Dependency:
    registry: dict[str, Callable] = {}

    def __init__(self, dependency: Callable) -> None:
        self.key = self._get_fn_hash(dependency)
        if self.key in self.registry:
            raise ValueError(f"Dependency with key {self.key} already exists")
        self.registry[self.key] = dependency

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        if self.key not in self.registry:
            raise ValueError(f"Dependency {self.key} not found")
        return self.registry[self.key](*args, **kwds)

    def _get_fn_hash(self, fn: Callable) -> str:
        module = fn.__module__
        qualname = fn.__qualname__
        code = fn.__code__

        return hashlib.sha256(f"{module}.{qualname}:{code.co_firstlineno}:{code.co_filename}".encode()).hexdigest()

    @contextmanager
    def override(self, overrider_dependency: Callable) -> None:
        self._override_key = self._get_fn_hash(overrider_dependency)
        self._original_dep = self.registry[self.key]

        self.registry[self.key] = overrider_dependency
        try:
            yield
        finally:
            self.registry[self.key] = self._original_dep
