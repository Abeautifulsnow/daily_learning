import argparse


def main():
    parser = argparse.ArgumentParser(description="")
    sub_parser = parser.add_subparsers(dest="sub_command", help="Sub-command to execute different func.")
    add_parser = sub_parser.add_parser("add", help="Add: x + y")
    multiply_parser = sub_parser.add_parser("multiply", help="Multiply: x * y")
    # common sub-command
    for common_parser in (add_parser, multiply_parser):
        common_parser.add_argument("-x", "--x",
                                   type=int,
                                   default=0
                                   )
        common_parser.add_argument("-y", "--y",
                                   type=int,
                                   default=0
                                   )

    args = parser.parse_args()

    result = 0
    if args.sub_command == "add":
        result = args.x + args.y
    if args.sub_command == "multiply":
        result = args.x * args.y

    print(f"Command: {args.sub_command} -> result: {result}")


if __name__ == '__main__':
    main()
