def reverse_positive_integer(x_input: int) -> int:
    hundreds_digit = x_input // 100
    ten_digit = (x_input - (hundreds_digit * 100)) // 10
    digits = x_input % 10

    new_integer = digits * 100 + ten_digit * 10 + hundreds_digit

    return new_integer


def reverse_positive_integer_2(x_input: int) -> int:
    str_integer = str(x_input)
    new_integer_str = str_integer[::-1]
    new_integer = int(new_integer_str)

    return new_integer


if __name__ == '__main__':
    x = int(input("Please input a three-digit integer: "))
    if len(str(x)) == 3:
        new_number = reverse_positive_integer_2(x)
        print("New number: ", new_number)
    else:
        print("Please input a three-digit integer.")
