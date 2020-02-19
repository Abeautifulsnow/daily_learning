import argparse
import pandas as pd


def csv_format(input_csv: str, out_csv: str):
    """
    This function is used to repair csv file.
    :param input_csv: csv format file that you need to input.
    :param out_csv: csv file that you need to output.
    :return: None.
    """
    data = pd.read_csv(input_csv)
    # drop col1 and col2.
    data = data.drop(columns=["col1", "col2"])
    # convert str type to list type and single quote to double quote.
    image_list = data["col3"].map(lambda x: "{}".format(x.split()).replace('\'', '\"'))
    # insert col4 to specified location.
    data.insert(loc=4, column="col4", value=image_list)
    data.to_csv(out_csv, mode="w", index=False)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="This script is used to format csv file.")
    parser.add_argument("-i", "--input_csv",
                        type=str,
                        default="",
                        help="This is an input csv format file.")
    parser.add_argument("-o", "--output_csv",
                        type=str,
                        default="",
                        help="This is an output csv format file.")
    args = parser.parse_args()
    csv_format(args.input_csv, args.output_csv)
