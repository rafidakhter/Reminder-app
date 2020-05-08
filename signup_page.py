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

#Parameters for creating connection with sql

# user email validation

def email_verification():
    ''' verify if the email is already in the system'''
    newuser= False

    while newuser == False:

        useremail_input = input('email?')
        useremail= ("'"+ useremail_input + "'") 

        #because of the "@" in the email PostgreSQL the query doesnt work so the email is entered as a string thus adding extra quotation marks 
        query = f'SELECT count(email) FROM registration WHERE email = {useremail}'

        return_text=execute_read_query(connection, query)

        if return_text[0][0]>0:
            print(f'The email {useremail_input} is alreay regestred in our system, please enter another email')
            pass
        else:
            newuser= True
            print('new user')
            return useremail_input
    pass
def password_check():
        ''' verify if the password is matching'''
    count = 0
    while count<1 :
        password = input('Password?')
        retype = input("retype password")

        if password !== retype:
            print('the retype password doesnt match')
            pass
        else:
            count =1
            return password
    pass

username= input('Name?')
useremail= email_verification()
password=password_check()

