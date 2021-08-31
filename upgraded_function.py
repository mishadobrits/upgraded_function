import math
from typing import Literal, Callable, Union


class LazyFunction:
    def __init__(self, func):
        self._ = self.func_ = func

        self.honest_get_attr = make_method("__getattribute__")
        self.call2 = make_method(self.func_)

    def __getattr__(self, item):
        if item[-1] == "_" and (item == "_" or item[-2] != "_"):
            return self.__dict__[item]
        else:
            return self.honest_get_attr(self, item)

    def __call__(self, *args):
        if any(type(arg) == type(self) for arg in args):
            return self.call2(*args)
        else:
            return self.func_(*args)


methods = [
    "__pos__",
    "__neg__",
    "__invert__",
    "__index__",
    "__abs__",
    "__invert__",
    "__round__",
    "__getitem__",
    "__setitem__",
    "__delitem__",
    "__cmp__",
    "__eq__",
    "__ne__",
    "__lt__",
    "__gt__",
    "__le__",
    "__ge__",
    "__iadd__",
    "__isub__",
    "__imul__",
    "__ifloordiv__",
    "__idiv__",
    "__itruediv__",
    "__imod_",
    "__ipow__",
    "__ilshift__",
    "__irshift__",
    "__iand__",
    "__ior__",
    "__ixor__",
    "__enter__",
    "__exit__",
    "__get__",
    "__set__",
    "__delete__",
    "__copy__",
    "__deepcopy__",
    "__iter__",
    "__next__",
]

method_names = {
    "call_": "__call__",
    "int_": "__int__",
    "bool_": "__bool__",
    "str_": "__str__",
    "len_": "__len__",
    "iter_": "__iter__",
}

functions = {
    "not_": lambda a: not a,
    "sum_": lambda a: sum(a),
    "min_": lambda a: min(a),
    "max_": lambda a: max(a),
    "list_": lambda a: list(a),
    "tuple_": lambda a: tuple(a),
    "str_": lambda a: str(a),
    "set_": lambda a: set(a),
    "any_": lambda a: any(a),
    "all_": lambda a: all(a),
    "__floor__": lambda a: math.floor(a),
    "__ceil__": lambda a: math.ceil(a),
    "__trunc__": lambda a: math.trunc(a),

}

rfunctions = {
    "__add__": lambda a, b: a + b,  # considers "__radd__"
    "__sub__": lambda a, b: a - b,
    "__mul__": lambda a, b: a * b,
    "__floordiv__": lambda a, b: a // b,
    "__lshift__": lambda a, b: a << b,
    "__rshift__": lambda a, b: a >> b,
    "__and__": lambda a, b: a and b,
    "__or__": lambda a, b: a or b,
    "__pow__": lambda a, b: a ** b,
    "__mod__": lambda a, b: a % b,
    "__xor__": lambda a, b: a | b,
}

for name, func in rfunctions.items():
    def set_func(name, func):
        functions[name] = func
        functions["__r" + name[2:]] = lambda a, b: func(b, a)
    set_func(name, func)



def make_method(method: Union[str, Callable]):
    # https://stackoverflow.com/a/19693065
    def _method(*args):
        def method_func(*func_args):
            nonlocal args
            args = list(args)
            for i, elem in enumerate(args):
                if type(elem) == LazyFunction:
                    args[i] = elem.func_(*func_args)

            if type(method) == type(lambda x: 1):
                # print(method, *func_args)
                return method(*args)
            else:
                code_str = f"{args[0]}.{method}({args[1:]})"
                # print(code_str)
                return eval(f"args[0].{method}(*args[1:])")

        return LazyFunction(method_func)
    return _method


for method_name in methods:
    _method = make_method(method_name)
    setattr(LazyFunction, method_name, _method)

for method_name, real_method_name in method_names.items():
    _method = make_method(real_method_name)
    setattr(LazyFunction, method_name, _method)


for method_name, function in functions.items():
    _method = make_method(function)
    setattr(LazyFunction, method_name, _method)



def lazyfunc_decorator(func):
    return LazyFunction(func)


arguments = LazyFunction(lambda *args: args)
arg, arg2, arg3, arg4, arg5 = [arguments[i] for i in range(5)]
arg1 = arg