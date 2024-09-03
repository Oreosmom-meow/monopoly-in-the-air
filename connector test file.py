import mysql.connector

def get_country_name(code):
    sql = f"select name, continent from country where iso_country = '{code}'"
    cursor = connection.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    if cursor.rowcount > 0:
        for row in result:
            print(f"For ICAO code: {code}, the country name is {row[0]}, the continent is {row[1]} .")
            return
connection = mysql.connector.connect(
    host="mysql.metropolia.fi",
    port=3306,
    user="yutongd",
    password="12345",
    database="yutongd"
    )

user_input = input("Enter a ICAO code: ")
get_country_name(user_input)