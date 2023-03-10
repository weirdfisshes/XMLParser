import psycopg2

from . import logs


class Database():
    def __init__(self, connection_string):
        self.connection_string = connection_string


def transaction(function):

    def wrapper(self, *args, **kwargs):
        try:
            connection = psycopg2.connect(self.connection_string)
            cursor = connection.cursor()
            result = function(self, cursor, *args, **kwargs)
            connection.commit()
        finally:
            connection.close()
        return result
    return wrapper


class FlowersDatabase(Database):
    @transaction
    def save_item(self, cursor, item):
        cursor.execute(f'''
            INSERT INTO flowers (code, name, group_name, price)
            VALUES ({item.code}, '{item.name}', '{item.group}', {item.price})
        ''')

        logs.logger.debug('Item saved')
