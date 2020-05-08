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


def login_verification():
    loggedin= False

    while loggedin == False:

        useremail_input =input('user email?') 
        useremail= ("'"+ useremail_input + "'")
        user_password = input('password?')
        userpassword= ("'"+ user_password + "'")

        #because of the "@" in the email PostgreSQL the query doesnt work so the email is entered as a string thus adding extra quotation marks 
        query = f'SELECT count(*) FROM registration WHERE email = {useremail} and password ={userpassword}'

        details_query= f'SELECT id,name FROM registration WHERE email = {useremail} and password ={userpassword} '


        return_text=execute_read_query(connection, query)

        if return_text[0][0]>0:
            user_detail=execute_read_query(connection, details_query)
            user_id = user_detail[0][0]
            name =user_detail[0][1]
            list_return=[user_id,name]
            print(f'Hi! {name}, you are logged in')
            return list_return
        else:
            print('Please type correct Email and Password or Sign up')

connection = create_connection(
    "reminder_app", "postgres", "password", "127.0.0.1", "5432")

userdetail=login_verification()