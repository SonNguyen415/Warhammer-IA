def zero():
    return "zero"


def one():
    return "one"


def two():
    return "two"


def three():
    return "three"


switcher = {
    0: zero,
    1: one,
    2: two,
    3: three,
}


def numbers_to_strings(argument):
    # Get the function from switcher dictionary
    func = switcher.get(argument, "nothing")
    # Execute the function
    return func()
