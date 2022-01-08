import sys
import types

# Dict that keeps track in modules
# TODO: Use singleton pattern to manager top level managers
class GlobalManager:
    def __init__(self, name, parent=None):
        self._name = name
        self._parent = parent
        self._full_name = name
        self._set_full_name()
        self._module = types.ModuleType(self._name)
        self._childs = {}

        sys.modules[]
    
    def _set_full_name(self):
        full_name = ""
        if self._parent:
            full_name += self._parent._full_name + "."
        full_name += self._name
        self._full_name = full_name
    
    def _inject_module(self):
        sys.modules.pop(self._full_name, None)
        self._set_full_name()
        for child in self._childs.values():
            child._inject_module()


    def get(self, __name: str, default=None):
        return self._childs.get(__name, default)

    def __setitem__(self, __name: str, __value) -> None:
        # Clean up before setting
        manager = GlobalManager(__name, self)

    def __getitem__(self, __name: str):
        return self._childs[__name]




def make_global_module(name):
    module = types.ModuleType(name)
    sys.modules[name] = module
    return module