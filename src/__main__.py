import sys
import logs
import time

import xml_parser
import database


def main():
    flower_parser = xml_parser.Parser()
    flower_database = database.FlowersDatabase('postgresql://localhost/finances?user=dbadmin&password=dbadmin')

    logs.logger.info('Script started')
    start_time = time.time()
    result = flower_parser.parse()

    try:
        for item in result:
            flower_database.save_item(item)
    except Exception as error:
        logs.logger.info(error)

    duration = time.time() - start_time
    logs.logger.info(f'Script finished, parse time: {duration}s')


if __name__ == '__main__':
    try:
        main()
    except BaseException:
        sys.exit(1)
