import pandas as pd
import os
from django.db import connection

def get_databases(conn):
    with conn.cursor() as cursor:
        cursor.execute("SELECT TOP 3 name, collation_name FROM sys.databases")
        row = cursor.fetchall()
        return row

def get_tables(conn):
    sql = "SELECT Distinct TABLE_NAME FROM information_schema.TABLES;"
    with conn.cursor() as cursor:
        cursor.execute(sql)
        row = cursor.fetchall()
        return row


def get_table_columns(conn,table_name):
    sql = "SELECT * FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = N'{}'".format(table_name)
    with conn.cursor() as cursor:
        cursor.execute(sql)
        row = cursor.fetchall()
        columns = [i[3] for i in row]
        return columns


def match_columns(col1,col2):
    passed = True
    for i in col1:
        if not i in col2:
            print(i)
            passed = False
    return passed


def get_table_columns(conn,table_name):
    sql = "SELECT * FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = N'{}'".format(table_name)
    with conn.cursor() as cursor:
        cursor.execute(sql)
        row = cursor.fetchall()
        columns = [i[3] for i in row]
        return columns


def insert_data(conn, tables_name, insert_columns, insert_values):
    sql = "insert into [{}]{} values {}".format(tables_name, insert_columns, insert_values)
    with conn.cursor() as cursor:
        cursor.execute(sql)


def main(file):
    databases_names = get_databases(connection)
    tables_names = get_tables(connection)
    columns_names = get_table_columns(connection, tables_names[1][0])
    insert_columns = "( [" + "],[".join(columns_names[1:]) + " ])"
    df = pd.read_excel(file, nrows=50,engine='openpyxl')

    for index, row in df.iterrows():

        temp_list = [str(i) for i in row]
        insert_values = "( N'" + "', N'".join(temp_list[1:]) + "' )"
        insert_data(connection, tables_names[1][0], insert_columns, insert_values)

    return df