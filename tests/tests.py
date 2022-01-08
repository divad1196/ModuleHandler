import ModuleHandler
from pathlib import Path
import types 
import sys

classes = ModuleHandler.ClassRegistry()
modules = ModuleHandler.ModuleRegistry(
    search_dirs=["tests_import_handler"]
)

my_test = ModuleHandler.make_global_module("my_test")
my_test.classes = classes
my_test.modules = modules

print(list(modules.keys()))

modules.init()
classes.init()