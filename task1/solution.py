from functools import wraps


def strict(func):
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
