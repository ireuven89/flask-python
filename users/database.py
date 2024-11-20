import os
import pathlib
import logging
from datetime import datetime
from uuid import uuid4
import pymysql

from utils.db import helpers

database = 'users'
databaseStatus = 'ok'
migrationsFolder = 'migrations'
dbConfig = {
    'host': 'users_db',
    'database': database,
    'user': 'root',
    'password': 'admin',
    'autocommit': True,
}

user = {
    'id': str,
    'name': str,
    'created_date': datetime,
    'updated_date': datetime,
}

def connect_db():
    try:
        db = pymysql.connect(**dbConfig)
        path = os.path.join(pathlib.Path().resolve(), migrationsFolder, "init_db.sql")
        logging.info(path)
        helpers.run_statements_from_file(path, db.cursor())
        global db_connection
        db_connection = db
        return 'connected'
    except pymysql.MySQLError as mse:
        logging.error("Unable to connect to database: %s", repr(mse))
        return 'failed to connect %s' % str(mse)
    except FileNotFoundError as e:
        logging.error("Unable migrate db  %s", repr(e))
        return 'failed to migrate DB: file not found'

def get_user(id):
    statement = 'select id, name, created_date, updated_date from users where id = %s'
    logging.debug(statement)
    cursor = db_connection.cursor()
    try:
        cursor.execute(statement, (id,))
        results = cursor.fetchall()
        for row in results:
            user['id'] = str(row[0])
            user['name'] = str(row[1])
            user['created_date'] = datetime.timestamp(row[2])
            user['updated_date'] = datetime.timestamp(row[3])
        logging.debug(user)
        return user
    except pymysql.MySQLError as mse:
        logging.error("Unable to fetch users: %s", repr(mse))
        raise mse
    except Exception as e:
        logging.error("Unable to fetch users: %s", repr(e))
        raise e
    finally:
        cursor.close()

# function get filters as tuple and db cursor and return users as dictionary from DB
def get_users(name):
    statement = 'select id, name, created_date, updated_date from users where name = %s order by id'
    logging.debug(statement)
    cursor = db_connection.cursor()
    result = []
    try:
        cursor.execute(statement, (name,))
        results = cursor.fetchall()
        for row in results:
            user['id'] = str(row[0])
            user['name'] = str(row[1])
            user['created_date'] = datetime.timestamp(row[2])
            user['updated_date'] = datetime.timestamp(row[3])
            result.append(user)
        logging.debug(results)
        return results
    except pymysql.MySQLError as mse:
        logging.error("Unable to fetch users: %s", repr(mse))
        raise mse
    except Exception as e:
        logging.error("Unable to fetch users: %s", repr(e))
        raise e
    finally:
        cursor.close()

# function create users in DB - return failed exception if not success
def create_users(users):
    results = []
    cursor = db_connection.cursor()
    for user in users:
        try:
            id = str(uuid4())
            statement = 'insert into users (id, name) values (%s, %s)'
            statement = statement % (id, user['name'])
            logging.debug(statement)
            cursor.execute(statement)
            result =  cursor.fetchone()
            results.append(result)
        except pymysql.MySQLError as mse:
            logging.error("failed to insert user: %s", repr(mse))
            raise mse
        except Exception as e:
            logging.error("failed to insert user: %s", repr(e))
            raise e
    cursor.close()

# function get filters as tuple and db cursor and return users as dictionary from DB
def update_users(users):
    results = []
    cursor = db_connection.cursor()
    for user in users:
        try:
            date = datetime.now()
            statement = 'update users set (name, updated_at) values(?, ?) where id = ?'
            cursor.execute(statement, (user['name'], date, user['id']))
            logging.debug(statement)
        except pymysql.MySQLError as mse:
            logging.error("failed updating user: %s", repr(mse))
            raise mse
        except Exception as e:
            logging.error("failed updating user: %s", repr(e))
            raise e
    cursor.close()

# function delete users in DB - return failed exception if not success
def delete_users(id):
    statement = 'delete from users where id = %s'
    cursor = db_connection.cursor()
    try:
        cursor.execute(statement, (id,))
    except pymysql.MySQLError as mse:
        logging.error("failed deleting user: %s", repr(mse))
        raise mse
    except Exception as e:
        logging.error("failed deleting user: %s", repr(e))
        raise e
    finally:
        cursor.close()

