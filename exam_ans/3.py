import math


def elephant_drink_number_of_buckets(depth: int, radium: int) -> int:
    water_capacity = 20 * 1000
    bucket_volume = math.pi * radium * radium * depth
    drink_number = water_capacity / bucket_volume

    if isinstance(drink_number, float):
        drink_number = int(drink_number) + 1

    return drink_number


if __name__ == '__main__':
    depth_of_bucket = int(input("Please enter the depth of bucket: "))
    radium_of_bucket = int(input("Please enter the radium of bucket: "))

    drink_bucket_nums = elephant_drink_number_of_buckets(depth_of_bucket, radium_of_bucket)
    print(drink_bucket_nums)
