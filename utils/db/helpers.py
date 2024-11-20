import logging
import pymysql


def run_statements_from_file(filePath, cursor):
    try:
        with (open(filePath) as sql_script):
            logging.info(filePath)
            sql_file = sql_script.read().strip()
            statements = filter(None, sql_file.split(';'))
            for statement in statements:
                statement = statement.replace('\n', "")
                cursor.execute(statement)
    except pymysql.MySQLError as mse:
        logging.error("Unable to run statement to database: %s", repr(mse))
        cursor.rollback()
        raise mse
    except Exception as e:
        raise e
    finally:
        cursor.close()


def run_single_statement(statement, params, connection):
    statement = statement.replace('\n', "").strip()
    logging.debug(statement)
    try:
        connection.cursor.execute(statement)
    except pymysql.MySQLError as mse:
        logging.error("failed to execute statement: %s", repr(mse))
        raise mse
    except Exception as e:
        raise e
