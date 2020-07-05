def main():
    int_num = int(input("Please input a number: "))

    if int_num % 2 == 0:
        print(f"{int_num} is a even num.")
    if int_num % 2 == 1:
        print(f"{int_num} is a odd num.")


if __name__ == '__main__':
    main()
