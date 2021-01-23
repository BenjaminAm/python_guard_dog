registered_plugins = {}


def call_with(node_class):
    def decorator_call_with(func):
        if node_class not in registered_plugins:
            registered_plugins[node_class] = {}
        if func.__name__ in registered_plugins[node_class]:
            raise ValueError("A function named %s already exists in registered_plugins[%s]. Please choose a unique "
                             "name for your plugin function. As good practice include the vulnerability type in the "
                             "function name." % (func.__name__, node_class))
        registered_plugins[node_class][func.__name__] = func
        return func
    return decorator_call_with
