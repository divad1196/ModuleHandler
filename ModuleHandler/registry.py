import os
from pathlib import Path
from typing import List, Union
from .module import Module

PathType = Union[Path, str]


class ModuleRegistry:
    def __init__(
        self,
        base_path: PathType = None,
        modules=[],
        search_dirs=[],
        module_class: type = Module,
    ):
        self.module_class = module_class
        if base_path is None:
            base_path = Path()
        self._base_path = Path(base_path).resolve()
        self._modules = {}
        self._search_dir = set()

        self.register_search_dirs(search_dirs, auto_register_modules=True)
        self.register_modules(modules)

    def path(self, path):
        return self._base_path.joinpath(path).resolve()

    def register_search_dirs(self, dirs, auto_register_modules=True):
        if not isinstance(dirs, (list, tuple)):
            dirs = [dirs]
        for d in dirs:
            path = self.path(d)
            self._search_dir.add(path)
            self.register_modules(
                [module.resolve() for module in path.iterdir()]
            )

    def register_modules(self, modules=[]):
        if not isinstance(modules, (list, tuple)):
            modules = [modules]
        for m in modules:
            module_path = self.path(m)
            # TODO: Check override?
            module = self.module_class(module_path, registry=self)
            self._modules[module.name] = module

    def reload_all(self):
        for module in self.values():
            module.load()

    def inject_all(self):
        for module in self.values():
            module.inject()

    def init(self):
        self.reload_all()

    def get(self, module: str, default=None):
        return self._modules.get(module, default)

    def __getitem__(self, module: str):
        return self._modules[module]

    def __iter__(self):
        return iter(self._modules)

    def items(self):
        return self._modules.items()

    def keys(self):
        return self._modules.keys()

    def values(self):
        return self._modules.values()
