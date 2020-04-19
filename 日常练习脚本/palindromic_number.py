import time


def distinguish_palindromic_number(number):
    if not number.isnumeric() or "-" in number or "." in number:
        print("Input data is not valid.")
    elif int(number) < 0:
        print("The number isn't a palindromic number.")
    elif int(number) == 0:
        print("This number is a palindromic number.")
    else:
        for i in range(len(number) // 2):
            if number[i] != number[-i - 1]:
                print("The number is not a palindromic number.")
                break
        else:
            print("The number is a palindromic number.")


def distinguish_palindromic_number_way_2(number):
    if not number.isnumeric() or "-" in number or "." in number:
        print("Input data is not valid.")
    elif int(number) < 0:
        print("The number isn't a palindromic number.")
    elif int(number) == 0:
        print("This number is a palindromic number.")
    else:
        if number[::-1] == number:
            print("The number is a palindromic number.")
        else:
            print("The number is not a palindromic number.")


if __name__ == "__main__":
    start = time.monotonic()
    input_number = input("Please input a number: ")
    distinguish_palindromic_number(input_number)
    distinguish_palindromic_number_way_2(input_number)
    end = time.monotonic()
    print(f"# Total time cost: {end-start} s")
