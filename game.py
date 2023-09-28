import mysql.connector

connection = mysql.connector.connect(
         host='127.0.0.1',
         port= 3306,
         database='flight_game',
         user='root',
         password='',
         autocommit=True
         )

def airports():
    sql = """SELECT iso_country, ident, name, type
    FROM airport
    WHERE type='large_airport'
    ORDER by RAND()
    LIMIT 20;"""                                  #?
    cursor = connection.cursor(dictionary=True)
    cursor.execute(sql)
    result = cursor.fetchall()
    return result

def new_game(player, place, t_limit, money):
    sql = """INSERT INTO game (name, location, time, bank) VALUES (%s, %s, %s, %s);"""
    cursor = connection.cursor(dictionary=True)
    cursor.execute(sql, (player, place, t_limit, money))