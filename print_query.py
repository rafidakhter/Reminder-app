import psycopg2
from psycopg2 import OperationalError

#connecting to the postgreSQL localserver
def create_connection(db_name, db_user, db_password, db_host, db_port):
    connection = None
    try:
        connection = psycopg2.connect(
            database=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port,
        )
        print("Connection to PostgreSQL DB successful")
    except OperationalError as e:
        print(f"The error '{e}' occurred")
    return connection

#Query function to create table  
def execute_read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except OperationalError as e:
        print(f"The error '{e}' occurred")


def print_items():

        user_id=1 
        location = 'walmart'
        name= 'Rafid'

        #because of the "@" in the email PostgreSQL the query doesnt work so the email is entered as a string thus adding extra quotation marks 
        query = f"SELECT count(*) item_name FROM saved_items WHERE user_id = '{user_id}' and purchase_location ='{location}'"

        item_query= f"SELECT item_name  FROM saved_items WHERE user_id = '{user_id}' and purchase_location ='{location}'"

        return_text=execute_read_query(connection, query)

        if return_text[0][0]>0:
            item=execute_read_query(connection, item_query)

            print(f'Hi! {name}, you are in{location}')
            print('you wated to purchase the following item:')
            for x in range(0,len(item)):
                print(' * '+ item[x][0])

        else:
            pass

connection = create_connection(
    "reminder_app", "postgres", "password", "127.0.0.1", "5432")

print_items()