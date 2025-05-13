import mysql.connector
import lib.config as config

mydb = mysql.connector.connect(
    host = config.DB_HOST,
    port = config.DB_PORT,
    user = config.DB_USER,
    password = config.DB_PWD,
    database = config.DB_DATABASE
)

mycursor = mydb.cursor()