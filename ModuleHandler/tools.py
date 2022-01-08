from importlib.machinery import SourceFileLoader
import types
from pathlib import Path
import sys


def make_global_module(name):
    module = types.ModuleType(name)
    sys.modules[name] = module
    return module

def _absolute_path_import(path: Path, name: str):
    loader = SourceFileLoader(name, str(path.resolve()))
    module = types.ModuleType(loader.name)
    loader.exec_module(module)
    return module

def absolute_path_import(path: Path, name=None):
    path = Path(path)
    name = name or path.stem
    if path.is_file():
        return _absolute_path_import(path.resolve(), name)
    if path.is_dir():
        init_file = path.joinpath("__init__.py")
        if init_file.is_file():
            return _absolute_path_import(init_file.resolve(), name)
    return
