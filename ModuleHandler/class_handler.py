

class ClassRegistry:
    def __init__(self, post_build_hooks=[], base_classes=tuple()):
        self._load_registry = {}  # Juste store classes in register order
        self._registry = {}       # Final classes after merge
        self._post_build_hooks = post_build_hooks
        self._base_classes = base_classes

    def _get_base_metaclass(self, name, *args, **kwargs) -> type:
        class Base(*self._base_classes):
            __abstract__ = True

        return Base

    def register(self, name, *args, **kwargs):
        def _register(cls: type) -> type:
            if name not in self._load_registry:
                base_class = self._get_base_metaclass(name, *args, **kwargs)
                self._load_registry[name] = [base_class]
            self._load_registry[name].append(cls)
            return cls
        return _register

    def _post_build(self, cls):
        """
            Meant to be overloaded.
            Apply hooks on the constructed class
        """
        for hook in self._post_build_hooks:
            cls = hook(cls)
        return cls

    
    def _build(self, name, classes):
        cls = type(
            name,
            tuple(reversed(classes)),
            {}
        )
        return self._post_build(cls)

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