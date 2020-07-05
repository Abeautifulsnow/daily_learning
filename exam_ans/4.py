def main(weight: int, char: str) -> int:
    basic_weight = 1000
    basic_fee = 8
    exceed_weight = weight - 1000
    remainder = exceed_weight % 500
    ratio = exceed_weight / 500

    if char == "n":
        basic_fee = basic_fee
    elif char == "y":
        basic_fee += 5

    if weight <= basic_weight:
        postage = basic_fee
    elif remainder != 0:
        exceed_rate = int(ratio) + 1
        postage = basic_fee + exceed_rate * 4
    else:
        postage = basic_fee + int(ratio) * 4

    return postage


if __name__ == '__main__':
    stuff_weight = int(input("Please enter the weight of stuff: "))
    char_emergency = str(input("Please enter a char 'y': expedite; or 'n': don't expedite: "))
    postage_stuff = main(stuff_weight, char_emergency)
    print(f"The postage of stuff: {postage_stuff}")
