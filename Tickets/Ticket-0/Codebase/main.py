from calculator import add, subtract, multiply, divide


def calculate_examples():
    return {
        "sum": add(2, 3),
        "difference": subtract(10, 4),
        "product": multiply(6, 7),
        "quotient": divide(20, 5),
    }


def main():
    results = calculate_examples()
    print("Simple calculator demo")
    for name, value in results.items():
        print(f"{name}: {value}")


if __name__ == "__main__":
    main()
