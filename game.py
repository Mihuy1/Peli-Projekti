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

def get_events():
    sql = "SELECT * FROM event;"
    cursor = connection.cursor(dictionary=True)
    cursor.execute(sql)
    result = cursor.fetchall()
    return result


def new_game(player, place, t_limit, money, a_ports):
    sql = """INSERT INTO game (name, location, time, bank) VALUES (%s, %s, %s, %s);"""
    cursor = connection.cursor(dictionary=True)
    cursor.execute(sql, (player, place, t_limit, money))

    events = get_events()
    event_id = {1: 0.3, 2: 0.2, 3: 0.4, 4: 0.1}
    id_list = []

    for i in range(0, 19):
        random_id = random.choices(list(event_id.keys()),
                                   list(event_id.values()))
        id_list.append(random_id[0])
    id_list.append(5)
    random.shuffle(id_list)

    e_ports = a_ports[1:].copy()
    random.shuffle(e_ports)


airports = get_airports()
