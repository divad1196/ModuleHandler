# ModuleHandler

If you want to create a plugable program, this library is made for you.

The goal of this library is to make easy the loading of selected modules among many availables from anywhere in the filesystem.
Of courses, you will need your modules to communicate, for exemple inherit a class from another module: There is tools for that too.



## Installation

```bash
pip3 install modulehandler
```



## Usage



```python
modules = ModuleHandler.ModuleRegistry(search_dirs=["dir_with_modules"])

my_test = modules.make_global("my_test") # Utility that creates a dynamic module named "my_test" with an object modules inside.
# See usage in modules below

# Load as many as you want
modules.load([  # Here, the codes of our modules will be executed
    "module1",
    "module2",
    "module3",
])
```



In one of your module, say module2, you will be able to refer to module1

```python
import my_test.modules import module1  # exists thanks to make_global_module
```



### ClasseRegistry

```
classes = ModuleHandler.ClassRegistry(post_build_hooks=[print_mro], base_classes=(BaseClass,))
modules = ModuleHandler.ModuleRegistry(search_dirs=["tests_import_handler"])

my_test = ModuleHandler.make_global_module("my_test")
print(list(sys.modules.keys()))
my_test.classes = classes
my_test.modules = modules

print(list(modules.keys()))

modules.init()

# Load as many as you want
m3 = modules["m3"].load()


classes.init()

A = classes["A"]
a = A()
```



# Future

* Currently, the configuration filename is not easily editable, same for configuration validation. It may be editable but still with current behaviour kept as default.