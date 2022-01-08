

class ClassRegistry:
    def __init__(self):
        self._load_registry = {}  # Juste store classes in register order
        self._registry = {}       # Final classes after merge

    def _get_base_metaclass(self, name, *args, **kwargs) -> type:
        class Base(self._base):
            __abstract__ = True

        return Base

    def register(self, name, *args, **kwargs):
        def _register(cls: type) -> type:
            if name not in self._load_registry:
                base_class = self._get_base_metaclass(name, *args, **kwargs)
                self._load_registry[name] = [base_class]
            self._load_registry[name].append(cls)
        return _register
    
    def _build(self, name, classes):
        return type(
            name,
            tuple(reversed(classes)),
            {}
        )

    def _make(self, name, classes):
        cls = self._build(name, classes)
        self._registry[name] = cls
        return cls

    def _make_class(self, name):
        classes = self._load_registry.get(name)
        # TODO: Handle missing
        return self._make(name, classes)

    def _make_register(self):
        self._registry = {}
        for name, classes in self._load_registry.items():
            self._make(name, classes)

    def __iter__(self):
        if self._registry:
            return iter(self._registry)
        return iter({})

    def __getitem__(self, model):
        return self._registry[model]

    def init(self):
        self._make_register()