from .registered_plugins import registered_plugins


def call_with(node_class):
    def decorator_call_with(func):
        if node_class not in registered_plugins:
            registered_plugins[node_class] = {}
        registered_plugins[node_class][func.__name__] = func
        return func
    return decorator_call_with
