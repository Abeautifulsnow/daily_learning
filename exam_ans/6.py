def allocate_pencil():
    pencil_nums = int(input("Please input the number of pencil: "))
    student_nums = int(input("Please input the number of student: "))
    average_pencils = pencil_nums // student_nums
    remaining_pencils = pencil_nums % student_nums

    print(f"Average pencils: {average_pencils}")
    print(f"Remaining pencils: {remaining_pencils}")


if __name__ == '__main__':
    allocate_pencil()
