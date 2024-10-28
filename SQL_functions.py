import random
import connector
import colors
import time

def insert_username(username,gamestart):
    sql = f"INSERT INTO game_sessions(player_name, money, start_time) VALUES ('{username}', 200, {gamestart});"
    cursor = connector.connection.cursor()
    cursor.execute(sql)

def get_session_id():
    sql2 = f'SELECT MAX(session_id) from game_sessions;'
    cursor = connector.connection.cursor()
    cursor.execute(sql2)
    result = cursor.fetchall()
    id = result[0][0]
    return id

def set_board_airports(session_id):
    airportnumbers = (2,4,5,7,8,10,13,15,16,19,20,21)
    i = 0
    start = time.time()
    country_sql = f'SELECT DISTINCT iso_country FROM airport GROUP BY iso_country HAVING COUNT(*) >= 3 ORDER BY RAND() LIMIT 4;'
    cursor = connector.connection.cursor()
    cursor.execute(country_sql)
    country_result = cursor.fetchall()
    for row in country_result:
        airport_sql = f'SELECT DISTINCT ident FROM airport WHERE iso_country = "{row[0]}" ORDER BY RAND() LIMIT 3;'
        cursor = connector.connection.cursor()
        cursor.execute(airport_sql)
        airport_result = cursor.fetchall()
        for airport in airport_result:
            sql = f'INSERT INTO player_property (airport_id, country_id, session_id, board_id) VALUES ("{airport[0]}", "{row[0]}", {session_id}, {airportnumbers[i]});'
#            sql = f'INSERT INTO session_airp_count (airport_id, country_id, session_id, board_id) VALUES ("{airport[0]}", "{row[0]}", {session_id}, {airportnumbers[i]});'
            cursor = connector.connection.cursor()
            cursor.execute(sql)
            i += 1
    end = time.time()
    print(f"Game database set up in {end - start} seconds.")
    return

#insert 12 new rows into player_property table without setting 3 random into bank owned
def set_player_property(session_id):
    airportnumbers = (2, 4, 5, 7, 8, 10, 13, 15, 16, 19, 20, 21)
    i = 0
    for x in airportnumbers:
        insert = f"INSERT IGNORE INTO player_property (session_id, board_id, ownership, upgrade_status) values ({session_id}, {airportnumbers[i]}, NULL, 0);"
        cursor = connector.connection.cursor()
        cursor.execute(insert)
        i += 1
    random_airport = random.choice(airportnumbers)
    select_country = f"select board_id from player_property where country_id in (select country_id from player_property where board_id = {random_airport}) and session_id = {session_id};"
    cursor = connector.connection.cursor()
    cursor.execute(select_country)
    country_result = cursor.fetchall()
    for row in country_result:
        update_bank = f"update player_property set ownership = 'bank' where board_id = {row[0]} and session_id = {session_id};"
        cursor = connector.connection.cursor()
        cursor.execute(update_bank)
    return

def check_owns_all_of_country(status) :
    sql1 = (f"SELECT country_id FROM player_property "
                             f"WHERE board_id = {status.position} "
                             f"AND session_id = {status.session_id};")
    cursor = connector.connection.cursor()
    cursor.execute(sql1)
    result = cursor.fetchall()
    if cursor.rowcount > 0:
        for row in result:
            country_id = row[0]
    sql2 = (f"SELECT COUNT(board_id) FROM  player_property  "
    #       f"LEFT JOIN session_airp_count s ON p.board_id = s.board_id "
           f"WHERE session_id = {status.session_id} " 
           f"AND ownership = '{status.username}' "
           f"AND country_id = '{country_id}'"
           f"AND session_id = {status.session_id};")
    cursor = connector.connection.cursor()
    cursor.execute(sql2)
    result = cursor.fetchall()
    if result[0][0] == 3:
        return True
    else:
        return False

def clear_tables(session_id):
    sql1 = f"DELETE FROM player_property where session_id = {session_id};"
   # sql2 = f"DELETE FROM player_property where session_id = {session_id};"
    cursor = connector.connection.cursor()
    cursor.execute(sql1)
   # cursor.execute(sql2)
    print(f"{colors.col.GREEN}Successfully deleted session:{session_id} related redundant tables.{colors.col.END}")

def get_country_name(status):
    sql = f"select name from country join player_property on iso_country = country_id WHERE player_property.session_id = {status.session_id} and player_property.board_id = {status.position};"
    cursor = connector.connection.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    if cursor.rowcount > 0:
        for row in result:
            country_name = row[0]
    return country_name

def get_all_country_name_and_number(status):
    country_names = []
    airport_numbers = []
    tempo_list = []
    sql2 = f"SELECT country_id, COUNT(board_id) AS airport_count FROM player_property where board_id = board_id AND session_id = session_id and session_id = {status.session_id}  AND ownership = '{status.username}' GROUP BY country_id;"
    cursor = connector.connection.cursor()
    cursor.execute(sql2)
    result2 = cursor.fetchall()
    if cursor.rowcount > 0:
        for key, value in result2:
            tempo_list.append(key)
            airport_numbers.append(value)
    for x in tempo_list:
        sql1 = f"SELECT DISTINCT(name) from country JOIN player_property on iso_country = country_id WHERE player_property.session_id = {status.session_id} and player_property.country_id = '{x}'; "
        cursor = connector.connection.cursor()
        cursor.execute(sql1)
        result1 = cursor.fetchall()
        if cursor.rowcount > 0:
            for row in result1:
                name = row[0]
                country_names.append(name)
    return (country_names, airport_numbers)

def get_airport_name(status):
    sql = f"select name from airport join player_property on ident = airport_id WHERE player_property.session_id = {status.session_id} and player_property.board_id = {status.position};"
    cursor = connector.connection.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    if cursor.rowcount > 0:
        for row in result:
            airp_name = row[0]
    return airp_name

def get_money(session_id): #Yutong
    sql = f"select money from game_sessions where session_id = {session_id}"
    cursor = connector.connection.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    if cursor.rowcount > 0:
        for row in result:
            money = row[0]
    return money

def get_airport_price(position):
    sql = f"select price from board where board_id = {position}"
    cursor = connector.connection.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    if cursor.rowcount > 0:
        for row in result:
            price = row[0]
    return price

def get_type_id(position):
    sql = f"select type_id from board where board_id = {position}"
    cursor = connector.connection.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    if cursor.rowcount > 0:
        for row in result:
            id = row[0]
    return id

def get_all_owned_airport(session_id,username):
    sql = f"select COUNT(ownership) from player_property where session_id = {session_id} and ownership = '{username}';"
    cursor = connector.connection.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    if cursor.rowcount > 0:
        for row in result:
            airport_number = row[0]
    return airport_number

def get_upgraded_airport_number(session_id):
    sql = f"select COUNT(ownership) from player_property where session_id = {session_id} and upgrade_status > 0"
    cursor = connector.connection.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    if cursor.rowcount > 0:
        for row in result:
            upgrade_number = row[0]
    return upgrade_number

def get_upgrade_status(status):
    sql = f"select upgrade_status from player_property where session_id = {status.session_id} and board_id = {status.position} "
    cursor = connector.connection.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    if cursor.rowcount > 0:
        for row in result:
            upgrade_status = row[0]
    return upgrade_status

def check_airport_owner(status):
    sql = f"select ownership from player_property where board_id = {status.position} and session_id = {status.session_id}"
    cursor = connector.connection.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    if cursor.rowcount > 0:
        for row in result:
            airport_owner = row[0]
    return airport_owner

'''def check_jail_card(session_id):
    sql = f"select out_of_jail_card from game_sessions where session_id = {session_id}"
    cursor = connector.connection.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    card_number = result[0][0]
    return card_number
'''
def modify_money(temp_money,session_id):
    update = f"update game_sessions set money = {temp_money} where session_id = {session_id}"
    cursor = connector.connection.cursor()
    cursor.execute(update)
    get_money(session_id)

def modify_owner_to_user(status):
    update = (f"update player_property set ownership = '{status.username}' where board_id = {status.position} and session_id = {status.session_id}")
    cursor = connector.connection.cursor()
    cursor.execute(update)

def cheat_owner_to_user(status):
    update = (f"update player_property set ownership = '{status.username}' where session_id = {status.session_id}")
    cursor = connector.connection.cursor()
    cursor.execute(update)

def modify_owner_to_bank(position,session_id):
    update = (f"update player_property set ownership = 'bank' where board_id = {position} and session_id = {session_id}")
    cursor = connector.connection.cursor()
    cursor.execute(update)

'''def modify_out_of_jail_card(jail_card,session_id):
    global username
    sql = f"update game_sessions set out_of_jail_card = '{jail_card}' where session_id = {session_id}"
    cursor = connector.connection.cursor()
    cursor.execute(sql)
'''
def modify_airport_status(position, temp_status,session_id):
    sql = f"update player_property set upgrade_status = {temp_status} where board_id = {position} and session_id = {session_id}"
    cursor = connector.connection.cursor()
    cursor.execute(sql)

def insert_high_score(session_id, score):
    sql = f"INSERT INTO high_score(session_id, score) VALUES ({session_id}, {score});)"
    cursor = connector.connection.cursor()
    cursor.execute(sql)


def get_top_high_score():
    session_list = []
    player_name = []
    high_score = []
    if not connector.connection.is_connected():
        connector.connection.reconnect(attempts=3, delay=5)
    sql = f'select session_id,score from high_score ORDER by score DESC limit 5'
    cursor = connector.connection.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    for id, score in result:
        session_list.append(id)
        high_score.append(score)
    for i in session_list:
        sql2 = f'select player_name from game_sessions where session_id = {i};'
        cursor.execute(sql2)
        result2 = cursor.fetchall()
        for name in result2:
            player_name.append(name[0])
    return(player_name, high_score,session_list)