import mysql.connector
from mysql.connector import Error
import math


def create_connection(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name
        )
        print("Connection to MySQL DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection
a = create_connection('betkill.beget.tech', 'betkill_bd_auto', 'Ubuntu18.04', 'betkill_bd_auto')


def execute_read_query(a, query, var):
    cursor = a.cursor()
    result = None
    try:
        cursor.execute(query, var)
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f"The error '{e}' occurred")


def execute_query(connection, query, var):
    connection.autocommit = True
    cursor = connection.cursor()
    try:
        cursor.execute(query, var)
    except OperationalError as e:
        print(f"The error '{e}' occurred")


def rp_additon(wl, rv, rp, avrp, alive):
    if wl == 1:
        if rp-avrp <= 0:
            change = int(100*rv+10*math.log(abs(rp-avrp)+1, 10)+alive*rv*10)
        else:
            change = int(100*rv-10*math.log(abs(rp-avrp)+1, 10)+alive*rv*10)
    elif wl == 0:
        if rp - avrp <= 0:
            change = int(-1.5*(100/rv)+10*math.log(abs(rp-avrp)+1, 10)+alive*rv*10)
        else:
            change = int(-1.5*(100/rv)-10*math.log(abs(rp-avrp)+1, 10)+alive*rv*10)
    if rp+change < 0:
        return '0'
    else:
        return str(change+rp)

def endgame(gamers):
    user_rp = []
    for gamer in list(gamers.keys()):
        select_users = "SELECT rp FROM users WHERE id_discord = %s"
        users = execute_read_query(a, select_users, (gamer,))
        for user in users:
            user = str(user)
            user = user[1:user.find(',')]
            user_rp.append(int(user))
    for gamer in list(gamers.keys()):
        select_users = "SELECT rp FROM users WHERE id_discord = %s"
        users = execute_read_query(a, select_users, (gamer,))
        for user in users:
            user = str(user)
            user = int(user[1:user.find(',')])
        rating = rp_additon(gamers[gamer][0], gamers[gamer][1], user, sum(user_rp)/len(user_rp), gamers[gamer][2])
        update_post_description = """
        UPDATE
         users
        SET
         rp = %s
        WHERE
         id_discord = %s
        """
        execute_query(a, update_post_description, (rating, gamer))
    for gamer in list(gamers.keys()):
        if gamers[gamer][0] == 1:
            select_users = "SELECT win FROM users WHERE id_discord = %s"
            users = execute_read_query(a, select_users, (gamer,))
            for user in users:
                user = str(user)
                user = int(user[1:user.find(',')])
            update_post_description = """
                UPDATE
                 users
                SET
                 win = %s
                WHERE
                 id_discord = %s
                """
            execute_query(a, update_post_description, (user+1, gamer))
        else:
            select_users = "SELECT lose FROM users WHERE id_discord = %s"
            users = execute_read_query(a, select_users, (gamer,))
            for user in users:
                user = str(user)
                user = int(user[1:user.find(',')])
            update_post_description = """
                UPDATE
                 users
                SET
                 lose = %s
                WHERE
                 id_discord = %s
                """
            execute_query(a, update_post_description, (user+1, gamer))