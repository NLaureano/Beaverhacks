def EVIL(a, b):
    return a + b


def EVIL2(a, b):
    return a - b


def EVIL3(a, b):
    return a * b


def EVIL4(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b
