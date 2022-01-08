import os
from pathlib import Path
from typing import List, Union, Any
from .module import Module
from .tools import make_global_module
import types 
import sys

PathType = Union[Path, str]

class ConflictBehaviour:
    error = 0
    ignore = 1
    override = 2

CB = ConflictBehaviour


class ModuleRegistryWrapper(types.ModuleType):
    def __init__(self, registry):
        self._registry = registry

    def __getattribute__(self, __name: str) -> Any:
        module = object.__getattribute__(self, "_registry").get(__name)
        if module:
            return module.load(reload=False)
        return object.__getattribute__(self, __name)

    # https://stackoverflow.com/questions/44162283/python-getattr-autocompletion
    # def __dir__(self):
    #     return 

    # def __dict__(self):
    #     return {
    #         name: module
    #         for name, module in
    #         object.__getattribute__(self, "_registry").items()
    #         if module.loaded
    #     }

class ModuleRegistry:
    def __init__(
        self,
        base_path: PathType = None,
        modules=[],
        search_dirs=[],
        module_class: type = Module,
        conflict_behaviour=CB.error
    ):
        self.module_class = module_class
        if base_path is None:
            base_path = Path()
        self._base_path = Path(base_path).resolve()
        self._modules = {}
        self._search_dir = set()
        self._cb = conflict_behaviour
        self._wrapper = ModuleRegistryWrapper(self)
        # self._global_module = (None, None)  # (name, object)

        self.register_search_dirs(search_dirs, auto_register_modules=True)
        self.register_modules(modules)

    def make_global(self, name=None, module=None):
        if module is None and name:
            module = make_global_module(name)
        elif module:
            name = module.__name__
        sys.modules[name + ".modules"] = module.modules = self.wrapper
        self._global_module = (name, module)
        return module

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
            if self._cb == CB.override or module.name not in self._modules:
                self._modules[module.name] = module
            elif self._cb == CB.error:
                raise Exception(
                    "Module loading name conflict:\n{old}\n{new}".format(
                        old=self._modules[module.name],
                        new=module
                    )
                )

    def load(self, modules):
        if not isinstance(modules, (tuple, list)):
            modules = [modules]
        return [
            self[m].load()
            for m in modules
        ]
            

    def reload_all(self):
        for module in self.values():
            module.load()

    def inject_all(self):
        for module in self.values():
            module.inject()

    def init(self):
        pass
    
    @property
    def wrapper(self):
        return self._wrapper

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
