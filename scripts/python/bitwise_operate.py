def add(num: int):
    # Add 1 to num.
    mask = 1
    # Iterate through each bit of the number
    while (num & mask) != 0:
        # Toggle the bit at the current position
        num ^= mask
        # Shift the mask to the next position
        mask <<= 1

    # Toggle the last bit to handle the case where all bits are 1
    num ^= mask
    return num


print(add(1))
print(add(10))
print(add(9))
print(add(7))
print(add(4))
print(add(8))
print(add(0))
