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
    def wrapper(*args):
        types_of_args = map(type, args)
        expected_types = func.__annotations__.values()

        for actual, expected in zip(types_of_args, expected_types):
            if actual != expected:
                raise TypeError(
                    f"Expected argument of type {expected.__name__}, but got {actual.__name__} instead"
                )

        return func(*args)

    return wrapper
