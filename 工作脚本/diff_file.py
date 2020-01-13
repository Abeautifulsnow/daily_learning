import difflib
import sys
import logging


def readfile(filename):
    try:
        fileHandle = open(filename, 'r')
        text = fileHandle.read().splitlines()
        fileHandle.close()
        return text
    except IOError as e:
        print("Read file error:", str(e))
        sys.exit()


if __name__ == "__main__":
    try:
        textfile1, textfile2 = sys.argv[1], sys.argv[2]
    except Exception as e:
        print("Error:", str(e))
        print("Usage: diff_file.py filename1 filename2 > diff.html")
        sys.exit()
    if textfile1 == "" or textfile2 == "":
        print("filename must be valid.")
        print("Usage: diff_file.py filename1 filename2 > diff.html")
        sys.exit()
    text1_lines = readfile(textfile1)
    text2_lines = readfile(textfile2)
    d = difflib.HtmlDiff()
    print(d.make_file(text1_lines, text2_lines))
