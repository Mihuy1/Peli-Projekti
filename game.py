import random
import story
import mysql.connector

from geopy import distance

connection = mysql.connector.connect(
         host='127.0.0.1',
         port= 3306,
         database='flight_game',
         user='root',
         password='',
         autocommit=True
         )
money = 10000
p_range = money*4

def get_airports():
    sql = """SELECT iso_country, ident, name, type, latitude_deg, longitude_deg
    FROM airport
    WHERE type='large_airport'
    ORDER by RAND()
    LIMIT 21;"""                                  #?
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
    g_id = cursor.lastrowid

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

    for i, event_id in enumerate(id_list):
        sql = "INSERT INTO events (location, event_id, game_id) VALUES (%s, %s, %s);"
        cursor = connection.cursor(dictionary=True)
        cursor.execute(sql, (e_ports[i]['ident'], event_id, g_id))
    return g_id


airports = get_airports()

# Get information about airport
def get_airport_info(icao):
    sql=f'''SELECT iso_country, ident, name, latitude_deg, longitude_deg
            FROM airport
            WHERE ident = %s'''
    cursor = connection.cursor(dictionary=True)
    cursor.execute(sql, (icao,))
    result = cursor.fetchall()

    return result



def airport_distance(current, target):
    start = get_airport_info(current)[0]  # Access the first (and only) item in the list
    end = get_airport_info(target)[0]  # Access the first (and only) item in the list
    start_coords = (start['latitude_deg'], start['longitude_deg'])
    end_coords = (end['latitude_deg'], end['longitude_deg'])
    return distance.distance(start_coords, end_coords).km

def airports_in_range(icao, a_ports, p_range):
    in_range = []
    for a_port in a_ports:
        dist = airport_distance(icao, a_port['ident'])
        if dist <= p_range and not dist == 0:
            in_range.append(a_port)
    return in_range

def check_event(g_id, cur_airport):
    sql = f'''SELECT events.id, event.id as event_id, events.game_id
    FROM events
    JOIN event ON event.id = events.event_id 
    WHERE game_id = %s 
    AND location = %s'''
    cursor = connection.cursor(dictionary=True)
    cursor.execute(sql, (g_id, cur_airport))
    result = cursor.fetchone()
    if result is None:
        return False
    return result


def update_location(g_id, name, icao, m, time):
    sql = '''UPDATE game SET name = %s, location = %s,  bank = %s, time = %s  WHERE id = %s'''
    cursor = connection.cursor(dictionary=True)
    cursor.execute(sql, (name, icao, money, time, g_id))


storyDialog = input('Do you want to read the background story? (Y/N): ')
if storyDialog == 'Y':
    for line in story.getStory():
        print(line)

print('When you are ready to start, ')
player = input('type player name: ')
t_limit = 0
while True:
    pet=input('What pet did you bring with you? Cat or dog?')
    if pet == "cat":
        t_limit = 240
        break
    elif pet == "dog":
        t_limit = 168
        break
    else:
        print('Sorry, you can only take a cat or a dog.')

# boolean for game over and win
game_over = False
win = False
money = 10000
p_range = money*4
score = 0
pet_found = False

# all airports
all_airports = get_airports()
# start_airport ident
s_airport = airports[0]['ident']

# current airport
current_airport = s_airport

game_id = new_game(player, s_airport, t_limit, money, airports)

# GAME LOOP
while not game_over:
    event = check_event(game_id, current_airport)
    airports = airports_in_range(current_airport, all_airports, p_range)
    print(f'''\033[34mThere are {len(airports)} airports in range: \033[0m''')
    if len(airports) == 0:
        print('You are out of range.')
        game_over = True
    while not game_over:
        # get current airport info
        airport = get_airport_info(current_airport)
        # show game status
        print(f"You are at {airport[0]['ident']} ({airport[0]['name']}).")
        print(f'''You have {money:.0f}$ and {t_limit} hours left to find a {pet}.''')
        print('Your pet is in one of these airports:')

        for i in range(len(all_airports)):
            ap_distance = airport_distance(current_airport, all_airports[i]["ident"])
            print(
                f'{i + 1}. {all_airports[i]["name"]}, icao: {all_airports[i]["ident"]}, distance: {ap_distance:.0f}km)')
        if p_range < 0:
            game_over = True
            # ask for destination
        dest = input("Where do you want to go? ICAO:")
        selected_distance = airport_distance(current_airport, dest)
        money -= selected_distance/4
        update_location(game_id, player, dest, money, t_limit)
        current_airport = dest
        if p_range < 0:
            game_over = True
    # if pet is found and player is at start, game is won
    if win and current_airport == s_airport:
        print(f'You are at {airport[0]["name"]}.')
        print(f'You have {money:.0f}$ and {t_limit} hours left to find a {pet}.')
        game_over = True











