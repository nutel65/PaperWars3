def wrap_func(func, *args, **kwargs):
    def wrapper():
        return func(*args, **kwargs)
    return wrapper

def add(arg1, arg2):
    return arg1 + arg2

wrapped = wrap_func(add, 3, 5)
print("wrapped", wrapped())

