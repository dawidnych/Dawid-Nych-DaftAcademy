def greetings(func):
    x = func()
    print("Hello " + x.lower().title())


@greetings
def name_surname():
    return "dawid nych"