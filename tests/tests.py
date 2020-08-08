import ModuleHandler
from pathlib import Path
registry = ModuleHandler.ModuleRegistry()

tests_import_handler = Path("tests_import_handler").resolve()
addons = tests_import_handler.joinpath("addons")
m2 = tests_import_handler.joinpath("m2")
m3 = tests_import_handler.joinpath("m3.py")

# Register won't load
registry.register_search_dir(addons)
registry.register_module(m2)
registry.register_module(m3)

# load modules individually
m3 = registry.load("m3")

# load all modules (will also reload already loaded modules)
registry.load_all()

# access loaded module
m1 = registry["m1"]
m4 = registry.get("m4")  # return None

# register + load
m2 = registry.import_module(m2)

# import from search paths if not already loaded
m1 = registry.imports("m1")
