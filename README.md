# ModuleHandler



## Installation

```bash
pip3 install modulehandler
```



## Usage

Considering this folder tree

```bash
tests_import_handler
├── addons
│   └── m1
│       ├── __init__.py
│       ├── manifest.json
│       └── README.md
├── m2
│   ├── __init__.py
│   └── manifest.json
└── m3.py
```

```python
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
m3 = registry.load("m3")  # ignore if already loader with noreload=True

# load all modules
registry.load_all()  # ignore if already loader with noreload=True

# access loaded module
m1 = registry["m1"]
m4 = registry.get("m4")  # return None

# register + load
m2 = registry.import_module(m2)

# import from search paths if not already loaded
m1 = registry.imports("m1")

# get readme as html
registry.description("m1")

# get module absolute path
registry.path("m1")
```

Nb:

* This won't change sys search paths nor add modules to sys.modules: `"m1" in sys.modules  # False`
* loading only replace module in registry but this won't propagate to copy of old module. 



# Future

* Currently, the configuration filename is not easily editable, same for configuration validation. It may be editable but still with current behaviour kept as default.