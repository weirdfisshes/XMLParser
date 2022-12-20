import sys
import time

from . import logs
from . import xml_parser
from . import database
from . import config


def main():
    flower_parser = xml_parser.Parser(config.PRICE_URL)
    flower_database = database.FlowersDatabase(config.DATABASE_URL)

    logs.logger.info('Script started')
    start_time = time.time()

    try:
        result, length, errors = flower_parser.parse()

    except Exception:
        logs.logger.error('Error while parsing')

        return

    try:
        for item in result:
            flower_database.save_item(item)

    except Exception:
        logs.logger.exception('Error while saving')

        return

    duration = time.time() - start_time
    logs.logger.info(
        f'Done, parse time: {round(duration)}s, '
        f'items received: {length}, invalid items: {errors}'
    )


if __name__ == '__main__':
    try:
        main()
    except BaseException:
        logs.logger.exception('Uncaught exception')
        sys.exit(1)
