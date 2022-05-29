from getpass import getpass
import mysql.connector


mydb = mysql.connector.connect(
    host="localhost",
    user=input("Enter username: "),
    password=getpass("Enter password: "),
)

#mydb = mysql.connector.connect(host = "127.0.0.1", user = "root", passwd = "Rhythm123R")
mycursor = mydb.cursor()
mycursor.execute("CREATE DATABASE Security")
mydb.commit()
mydb.connect(database = "Security")
mycursor.execute("CREATE TABLE Security(NAME VARCHAR(50), DATE_JOINING DATE, DEPARTMENT VARCHAR(50));")
mydb.commit()
