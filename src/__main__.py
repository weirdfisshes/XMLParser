import os
import sys

import xml_parser


def main():
    print('start')
    flower_parser = xml_parser.Parser()
    file_path = os.getcwd() + '/src/test_file.xml'
    result = flower_parser.parse(file_path)
    print(result)


if __name__ == '__main__':
    try:
        main()
    except BaseException:
        sys.exit(1)
