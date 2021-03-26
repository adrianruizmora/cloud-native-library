import mysql.connector
import json
import os


config_sql = {
  'host':os.environ['HOST_SQL_AZURE'],
  'user':os.environ['USER_SQL_AZURE'],
  'password':os.environ['PASSWORD_SQL_AZURE'],
  'database':os.environ['DATABASE_SQL_AZURE'],
  'client_flags': [mysql.connector.ClientFlag.SSL],
  'ssl_ca': os.environ["SSL_CA_SQL_AZURE"]}


    
def list_book():
    
    request = cursor.execute("""SELECT titre
    From library""")
    result = cursor.fetchall()
    print(json.dumps(result))


def list_book_like(titre):

    request = cursor.execute("""SELECT titre
    From library WHERE titre like "%s" """, (titre))
    result = cursor.fetchall()
    print(json.dumps(result))


conn = mysql.connector.connect(**config_sql)
cursor = conn.cursor(dictionary=True)
list_book()
list_book_like('Me')

