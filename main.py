import re


# 2.1
def greetings(func):
    def decorated_greetings(*args):
        tmp = func(*args)
        return f"Hello {tmp.lower().title()}"
    return decorated_greetings


@greetings
def name_surname():
    return "dawid nych"


# print(name_surname())


# 2.2
def is_palindrome(func):
    def checker(*args):
        regex = re.compile('[^a-zA-Z0-9]')
        tmp = regex.sub('', func(*args)).lower()
        if tmp == tmp[::-1]:
            return f"{func(*args)} - is palindrome"
        else:
            return f"{func(*args)} - is not palindrome"
    return checker


@is_palindrome
def sentence():
    return "annA"

# print(sentence())


# 2.3
def format_output(*args):
    def real_format(func):
        def wrapper(*arg):
            tmp = func(*arg)
            tmp_str = ""
            result_dict = {}
            for arg in args:
                if arg in tmp:
                    result_dict[arg] = tmp.get(arg)
                elif "__" in arg:
                    tmp_lst = arg.split("__")
                    for item in tmp_lst:
                        if item in tmp:
                            tmp_str += f"{tmp[item]} "
                        else:
                            raise ValueError("ValueError exception thrown")
                    result_dict[arg] = tmp_str.rstrip()
                else:
                    raise ValueError("ValueError exception thrown")
            return result_dict
        return wrapper
    return real_format


@format_output("first_name__last_name", "city")
def first_func():
    return {
        "first_name": "Jan",
        "last_name": "Kowalski",
        "city": "Warszawa"
    }


@format_output("first_name", "age")
def second_func():
    return {
        "first_name": "Jan",
        "last_name": "Kowalski",
        "city": "Warszawa"
    }


# print(first_func())
# print(second_func())


# 2.4
class A:
    pass


def add_class_method(cls):
    def wrapper(func):
        setattr(cls, func.__name__, func)
        return func
    return wrapper


@add_class_method(A)
def foo():
    return "Hello!"


def add_instance_method(cls):
    def wrapper(func):
        def instance_method(self, *args, **kwargs):
            return func(*args, **kwargs)
        o = cls()
        cls2 = o.__class__
        o2 = cls2
        setattr(o2, func.__name__, instance_method)
        return func
    return wrapper


@add_instance_method(A)
def bar():
    return "Hello again!"


print(A.foo())
print(A().bar())
assert A.foo() == "Hello!"
assert A().bar() == "Hello again!"

