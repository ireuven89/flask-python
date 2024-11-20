import logging
import os
from uuid import uuid4

import pymysql
import pathlib

import utils.db.helpers

database = 'items'
migrationsFolder = 'migrations'
dbConfig = {
    'host': 'items_db',
    'database': database,
    'user': 'root',
    'password': 'admin',
}

def connect_db():
    try:
        db = pymysql.connect(**dbConfig)
        db_cursor = db.cursor()
        path = os.path.join(pathlib.Path().resolve(), migrationsFolder, "init_db.sql")
        logging.info(path)
        global db_connection
        db_connection = db
        utils.db.helpers.run_statements_from_file(path, db_cursor)
        return 'connected'
    except pymysql.MySQLError as e:
        logging.error("Unable to connect to database: %s", repr(e))
        return 'failed to connect'
    except Exception as e:
        logging.error("Unable migrate db  %s", repr(e))
        return 'failed to migrate DB: file not found'


def get_item(id):
    statement = 'select * from items where id = %s'
    cursor = db_connection.cursor()
    try:
        cursor.execute(statement, (id,))
        result = cursor.fetchall()
        return result
    except pymysql.MySQLError as mse:
        logging.error("Unable to get item: %s", mse)
        raise mse
    except Exception as e:
        logging.error("Unable to get item: %s", e)
        raise e


def get_items(name):
    statement = 'select * from items where name = %s order by name'
    results = []
    cursor = db_connection.cursor()
    try:
        cursor.execute(statement, (name,))
        for row in cursor:
            results.append(row)
        return results
    except pymysql.MySQLError as mse:
        logging.error("Unable to get item: %s", mse)
        raise mse


def insert_items(items):
    statement = 'insert into items (id, name, download_link) values (%s, %s, %s)'
    cursor = db_connection.cursor()
    success = []
    failed = []
    for item in items:
        try:
            id = uuid4()
            cursor.execute(statement, (id, item['name'], item['download_link']))
            success.append(cursor.fetchone())
            return success
        except pymysql.MySQLError as mse:
            logging.error("Unable to update item: %s", repr(mse))
        except Exception as e:
            logging.error("Unable to update item: %s", e)


def update_items(items):
    statement = 'update items set name = %s, download_link = %s where id = %s'
    cursor = db_connection.cursor()
    success = []
    failed = []
    for item in items:
        try:
            cursor.execute(statement, (item['name'], item['download_link'], item['id']))
            cursor.fetchone()
            success.append(item['id'])
        except pymysql.MySQLError as mse:
            failed.append(item['id'])
            logging.error("Unable to update item: %s", repr(mse))
        except Exception as e:
            failed.append(item['id'])
            logging.error("Unable to update item: %s", e)


def delete_item(items):
    statement = 'delete from items where id = %s'
    cursor = db_connection.cursor()

    for item in items:
        try:
            cursor.execute(statement, (item['id'],))
            cursor.fetchone()
        except pymysql.MySQLError as e:
            logging.error("failed to delete item: %s, %s", item['id'], repr(e))
        except Exception as e:
            logging.error("failed to delete item: %s, %s", item['id'], repr(e))

