import mysql.connector
connection = mysql.connector.connect(
    user="yutongd",
    password="12345",
    host="mysql.metropolia.fi",
    port=3306,
    database="yutongd",
    connection_timeout=60,
    autocommit = True
)
def run(sql) :
    cursor = connection.cursor()
    cursor.execute(sql)
    try :
        return cursor.fetchall()
    except :
        return None

sql = (f"SELECT UNIQUE COUNT(p.board_id) AS airport_count FROM player_property p "
       f"LEFT JOIN session_airp_count sa ON p.board_id = sa.board_id "
       f"AND p.session_id = sa.session_id "
       f"WHERE p.session_id = 1251 "
       f"AND p.ownership = 'robi' "
       f"GROUP BY sa.country_id;")
result = run(sql)
