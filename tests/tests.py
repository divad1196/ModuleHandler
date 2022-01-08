import ModuleHandler
from pathlib import Path
import sys


class BaseClass:
    foo = True

def print_mro(cls):
    print(cls.mro())
    return cls

classes = ModuleHandler.ClassRegistry(post_build_hooks=[print_mro], base_classes=(BaseClass,))
modules = ModuleHandler.ModuleRegistry(search_dirs=["tests_import_handler"])

# my_test = ModuleHandler.make_global_module("my_test")
# print(list(sys.modules.keys()))
# my_test.classes = classes
# sys.modules["my_test.modules"] = my_test.modules = modules.wrapper

my_test = modules.make_global("my_test")
my_test.classes = classes

print(list(modules.keys()))

modules.init()

# Load as many as you want
m3 = modules["m3"].load()



classes.init()

A = classes["A"]
a = A()


assert A.__name__ == "A"
assert a.a == 1
assert a.b == 2
assert a.c == 3
assert a.d == 3
