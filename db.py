# -*- coding: utf8 -*-

import sqlite3
import logging
from logging import FileHandler, DEBUG

import config

conn = None
cursor = None

logging.basicConfig(format='%(asctime)s - %(name)s - %(lineno)d - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

def db_connect():
    global conn
    global cursor
    conn = sqlite3.connect(config.db_file, check_same_thread=False)
    cursor = conn.cursor()
    logger.info("The sqlite connected")

def db_disconnect():
    if conn:
        cursor.close()
        conn.close()
        logger.info("The sqlite connection is closed")

def db_add_new(id: int, cur: str):
    if db_dont_find(id): # don't find
        logger.info("Add new id = " + str(id) + " cur = " + str(cur))
        cursor.execute('INSERT INTO currency (id, cur) VALUES (?, ?)', (id, cur))
        conn.commit()
        logger.info("Added new id = " + str(id) + " cur = " + str(cur))
    else: # find
        logger.info("Id already exists. Id = " + str(id))

def db_get_cur(id: int):
    if db_dont_find(id): # don't find
        db_add_new(id, config.DEFAULT_CUR)
        return config.DEFAULT_CUR
    else: # find
        try:
            sql_select_query = """select * from currency where id = ?"""
            cursor.execute(sql_select_query, (id,))
            records = cursor.fetchall()
            # print("Printing ID ", id)
            # for row in records:
            #     print("Currency = ", row[1])
            #     print("Description  = ", row[2])
            logger.info("Return for " + str(id) + " cur: " + str(records[0][1]))
            return records[0][1]
        except sqlite3.Error as error:
            logger.error("Failed to read data from sqlite table", error)

def db_update_value(id: int, currency: str):
    logger.info("Set for " + str(id) + " value cur = " + str(currency))
    if db_dont_find(id): # don't find
        db_add_new(id, config.DEFAULT_CUR)
    try:
        sql_update_query = """Update currency set cur = ? where id = ?"""
        data = (currency, id)
        cursor.execute(sql_update_query, data)
        conn.commit()
        logger.info("Setted for " + str(id) + " value cur = " + str(currency))
    except sqlite3.Error as error:
        logger.error("Failed to update sqlite table", error)

def db_update_values(id: int, currency: str, desc: str):
    logger.info("Set for " + str(id) + " value cur = " + str(currency) + " desc = " + str(desc))
    try:
        sql_select_query = """Update new_developers set cur = ?, desc = ? where id = ?"""
        columnValues = (currency, desc, id)
        cursor.execute(sql_select_query, columnValues)
        conn.commit()
    except sqlite3.Error as error:
        logger.error("Failed to update multiple columns of sqlite table", error)

def db_delete_row(id: int):
    logger.info("Delete " + str(id))
    try:
        sql_update_query = """DELETE from currency where id = ?"""
        cursor.execute(sql_update_query, (id,))
        conn.commit()
        logger.info("Deleted " + str(id))
    except sqlite3.Error as error:
        logger.error("Failed to delete row from table", error)

def db_dont_find(id: int):
    logger.info("Find " + str(id))
    try:
        sql_update_query = """SELECT * from currency where id = ?"""
        cursor.execute(sql_update_query, (id,))
        res = cursor.fetchall()
        if res == []:
            return True
        else:
            return False
    except sqlite3.Error as error:
        logger.error("Failed to find id from table", error)

def dp_print_table():
    try:
        sql_update_query = """SELECT * from currency"""
        cursor.execute(sql_update_query)
        res = cursor.fetchall()
        print(res)
    except sqlite3.Error as error:
        logger.error("Failed to print table", error)

# db_connect()
# dp_print_table()
# db_dont_find(353383641)
# db_delete_row(368696588)
# db_add_new(4, 123)
# db_update_value(3, 1)
# print(db_get_cur(4))
# db_disconnect()
