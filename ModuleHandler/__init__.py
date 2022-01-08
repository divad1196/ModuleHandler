from .registry import ModuleRegistry, CB, ConflictBehaviour
from .module import AbstractModule, Module
from .class_handler import ClassRegistry
from .tools import absolute_path_import, make_global_module


def setup(
    global_name,
    modules2load=[],

    # ModuleRegistry parameters
    base_path=None,
    modules=[],
    search_dirs=[],
    module_class: type = Module,
    conflict_behaviour=CB.error,

    # ClassRegistry parameters
    post_build_hooks=[],
    base_classes=tuple()
):
    classes = ClassRegistry(
        post_build_hooks=post_build_hooks,
        base_classes=base_classes,
    )
    modules = ModuleRegistry(
        base_path=base_path,
        modules=modules,
        search_dirs=search_dirs,
        module_class=module_class,
        conflict_behaviour=conflict_behaviour
    )

    module = make_global_module(global_name)
    module.classes = classes
    module.modules = modules

    # modules.init()
    modules.load(modules2load)
    classes.init()
    return module
