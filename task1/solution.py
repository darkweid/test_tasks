from functools import wraps


def strict(func):
    """
    A decorator that checks if the types of arguments passed to a function
    match the types declared in the function's type annotations.

    Args:
        func (function): The function to be decorated.

    Returns:
        function: A wrapper function that performs type checking before calling the original function.

    Raises:
        TypeError: If any argument type does not match the declared type in the function's annotations.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        expected_types = func.__annotations__

        # Check types for positional arguments (args)
        for i, (actual, expected) in enumerate(zip(args, list(expected_types.values())[:len(args)])):
            if actual.__class__ != expected:
                raise TypeError(
                    f"Expected positional argument {i + 1} of type {expected.__name__}, "
                    f"but got {actual.__class__.__name__} instead"
                )

        # Check types for keyword arguments (kwargs)
        for key, actual in kwargs.items():
            if key in expected_types:
                expected = expected_types[key]
                if actual.__class__ != expected:
                    raise TypeError(
                        f"Expected argument '{key}' of type {expected.__name__}, "
                        f"but got {actual.__class__.__name__} instead"
                    )
            else:
                raise TypeError(
                    f"Unexpected keyword argument '{key}'"
                )

        return func(*args, **kwargs)

    return wrapper
