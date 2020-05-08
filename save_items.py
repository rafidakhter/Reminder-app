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

#query for modifying database
def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        print("Query executed successfully")
    except OperationalError as e:
        print(f"The error '{e}' occurred")

    connection.commit()

connection = create_connection(
    "reminder_app", "postgres", "password", "127.0.0.1", "5432")
# this will be input section in the screen after log in

#funtion to save item 
def save_new_item():
    for x in range (0,5):
        status = input('save new item? y/n: ')
        if status == 'y':
            user_id = 1 #collectd from login page
            item = input('Item to save? ')
            location = input('where do you want to be riminded?  ')

            query_save_item=f''' 
                        INSERT INTO  
                        saved_items (user_id, item_name, purchase_location)
                        
                        VALUES
                        ('{user_id}','{item}','{location}');'''

            submit=input('submit item y/n? ')

            if submit == 'y':
                execute_query(connection,query_save_item)
        x+=1
            
save_new_item()