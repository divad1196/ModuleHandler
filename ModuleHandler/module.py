from pathlib import Path
from .tools import absolute_path_import
import sys
import json

class AbstractModule:
    def __init__(self, path, autoload=False, registry=None):
        """
            Abstract Representation of a module. By default, the python code is not loaded automaticaly.
        """
        self._registry = registry
        self._path = Path(path).resolve()
        self._name = self._path.stem
        self._module = None
        self._config = {}
        if autoload:
            self.load()

    @property
    def name(self, reload=True):
        if reload or not self._module:
            self._module = absolute_path_import(self.path)
        return self._name

    @property
    def path(self):
        return self._path

    @property
    def registry(self):
        return self._registry

    @property
    def config(self):
        return self._config

    def load(self, reload=True, **kw):
        """
            Load the module has python
        """
        if reload or not self._module:
            self._module = absolute_path_import(self.path)
        return self._module

    def inject(self, reload=True):
        module = self.load(reload=reload)
        sys.modules[self.name] = module


class Module(AbstractModule):
    config_name = "manifest.json"
    def __init__(self, path, autoload=False, registry=None):
        super(Module, self).__init__(path, autoload=autoload, registry=registry)
        self.reload_config()
        self._name = self.config.get("name", self._name)
        
    
    def reload_config(self):
        conf = self.path.joinpath(self.config_name)
        if conf.is_file():
            with open(conf) as f:
                self._config = json.load(f)
    
    def load(self, reload=True, check_dep=True, **kw):
        # Does not handle recursive dependences
        if check_dep:
            depends = self.config.get("depends", [])
            for dep in depends:
                self.registry[dep].load(reload=False)
        return super(Module, self).load(reload=reload)
