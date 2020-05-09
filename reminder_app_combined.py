import requests
import urllib.request
import json
import psycopg2
from psycopg2 import OperationalError

#-------------------------------------------xxxxxx---------------------------------------------------#

#The following function is to communicate with localy stored postgresql database called reminder app:
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
#Query function to read from table  
def execute_read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except OperationalError as e:
        print(f"The error '{e}' occurred")
#query for modifying database
def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        print("Query executed successfully")
    except OperationalError as e:
        print(f"The error '{e}' occurred")

    connection.commit()
#local database connection inputs:
connection = create_connection(
    "reminder_app", "postgres", "password", "127.0.0.1", "5432")
#-------------------------------------------xxxxxx---------------------------------------------------#
#functions for signing up:
def email_verification(connection):
    ''' verify if the email is already in the system'''
    newuser= False

    while newuser == False:

        useremail_input = input('email?')
        useremail= ("'"+ useremail_input + "'") 

        #because of the "@" in the email PostgreSQL the query doesnt work so the email is entered as a string thus adding extra quotation marks 
        query = f'SELECT count(*) FROM registration WHERE email = {useremail}'

        return_text=execute_read_query(connection, query)

        if return_text[0][0]>0:
            print(f'The email {useremail_input} is alreay regestred in our system, please enter another email')
            pass
        else:
            newuser= True
            print('new user')
            return useremail_input
def password_check():
    ''' verify if the password is matching'''
    count = 0
    while count<1 :
        password = input('Password?')
        retype = input("retype password")

        if password != retype:
            print('the retype password doesnt match')
            pass
        else:
            count =1
            return password
def add_data_registration(u_n,u_e,passw,con):
    submitted = False
    while submitted == False:

        submit = input('type yes to submit y/n?')

        if submit.lower()[0] == 'y':
            u_n="'"+u_n+"'"
            u_e="'"+u_e+"'"
            passw= "'"+passw+"'"

            query=f''' 
            INSERT INTO  
            registration (name, email,password)
            
            VALUES
            ({u_n},{u_e},{passw});'''
            execute_query(connection,query)

            submitted = True
#-------------------------------------------xxxxxx---------------------------------------------------#
# function for loggin in
def login_verification(connection):
    ''' verifies existing member or not, 
    upon sucessful login returns a list [user_id,user_name]'''
    loggedin= False

    while loggedin == False:

        useremail_input =input('user email?') 
        useremail= ("'"+ useremail_input + "'")
        user_password = input('password?')
        userpassword= ("'"+ user_password + "'")

        #because of the "@" in the email PostgreSQL the query doesnt work so the email is entered as a string thus adding extra quotation marks 
        query = f'SELECT count(*) FROM registration WHERE email = {useremail} and password ={userpassword}'

        details_query= f'SELECT id,name FROM registration WHERE email = {useremail} and password ={userpassword} ' #the two queries can be combined together

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
#-------------------------------------------xxxxxx---------------------------------------------------#

#funtion to save new item 
def save_new_item(u_id,connection):
    new_item =True
    while new_item== True:
        status = input('save new item? y/n: ')
        if status == 'y':
            user_id = u_id #collectd from login page
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
        else:
            new_item=False
#-------------------------------------------xxxxxx---------------------------------------------------#
#function to get users current location 
# comment because do not want to continuously call on google API and be charged
def get_user_location():
    '''-take these quote mars off when using
    'uses the google url post to get users location[long,lat,acuracy]'
    APIKEY='AIzaSyB4BdrazYRTttzy6H5XAu6ib7uL87bvgjk'
    url_requested= f'https://www.googleapis.com/geolocation/v1/geolocate?key={APIKEY}'
    response = requests.post( url_requested)
    r=response.text
    x=json.loads(r)
    lat=x['location']['lat']
    lng=x['location']['lng']
    accu=x['accuracy']
    user_location=[lat,lng,accu]
    print(user_location)
    '''
    #for test purposes:
    user_location= [45.3912876, -75.7549387,13]
    return user_location
#-------------------------------CHECK INSIDE STORE FUNCTION---------------------------------------------------#
# mock api result

def get_nearby_response_true(loc):
    loblaws={
            "html_attributions": [],
            "results": [
                    {
                        "business_status": "OPERATIONAL",
                        "geometry": {
                                "location": {
                                    "lat": 45.4299644,   
                                    "lng": -75.6837012
                                },
                                "viewport": {
                                    "northeast": {
                                            "lat": 45.43141677989273,
                                            "lng": -75.68274427010726
                                    },
                                    "southwest": {
                                            "lat": 45.42871712010728,
                                            "lng": -75.68544392989271
                                    }
                                }
                        },
                        "icon": "https://maps.gstatic.com/mapfiles/place_api/icons/shopping-71.png",
                        "id": "a68a855a3028e427afd712e88c241c565065d9e7",
                        "name": "Loblaws",
                        "opening_hours": {
                                "open_now": True
                        },
                        "photos": [
                                {
                                    "height": 3056,
                                    "html_attributions": [
                                            "<a href=\"https://maps.google.com/maps/contrib/113073450595369735649\">Steve Brandon</a>"
                                    ],
                                    "photo_reference": "CmRaAAAAvsiXU9o5GwhmUYKImQw055TNXmDQNUGbzdByNdo8bW0s1qwnP3yY2M0pl2-a66GqRcyYM9PQlmCGKPrFfMg4ktn9FQ2hqMyNL6jDFSQSc6x-pcMOPOtRBMjuzX2_pthhEhDutCBWp1C12U9-gHmUlP1YGhRI94rtkKd6HowaVaNkyLcpGdeJmA",
                                    "width": 4592
                                }
                        ],
                        "place_id": "ChIJff67xgQFzkwRMXfFBwUKEJA",
                        "plus_code": {
                                "compound_code": "C8H8+XG Lower Town, Ottawa, ON",
                                "global_code": "87Q6C8H8+XG"
                        },
                        "rating": 4.1,
                        "reference": "ChIJff67xgQFzkwRMXfFBwUKEJA",
                        "scope": "GOOGLE",
                        "types": [
                                "grocery_or_supermarket",
                                "pharmacy",
                                "bakery",
                                "food",
                                "health",
                                "point_of_interest",
                                "store",
                                "establishment"
                        ],
                        "user_ratings_total": 1607,
                        "vicinity": "363 Rideau St, Ottawa"
                    },
                    {
                        "business_status": "OPERATIONAL",
                        "geometry": {
                                "location": {
                                    "lat": 45.4294445,
                                    "lng": -75.6648447
                                },
                                "viewport": {
                                    "northeast": {
                                            "lat": 45.43097647989272,
                                            "lng": -75.66352652010728
                                    },
                                    "southwest": {
                                            "lat": 45.42827682010728,
                                            "lng": -75.66622617989272
                                    }
                                }
                        },
                        "icon": "https://maps.gstatic.com/mapfiles/place_api/icons/shopping-71.png",
                        "id": "fb7a599e822ce0bf418fd10540da009a609f36d4",
                        "name": "Loblaws",
                        "opening_hours": {
                                "open_now": True
                        },
                        "photos": [
                                {
                                    "height": 2358,
                                    "html_attributions": [
                                            "<a href=\"https://maps.google.com/maps/contrib/104730928604271663010\">Francisco Alvarez</a>"
                                    ],
                                    "photo_reference": "CmRaAAAAtQVNRrchQ4G061_mIUImlXS7t9nXJgm1SgYelMM8h5vvraPIb10b_pSAQLebgSLWVSIlauB8Jdq9l8vEx0ORMiSVpy-yJJ_Pg4zoEqtCNg_0FiVZvKad0to3PpBCfW2CEhC7JZDoz_HBgo8gpsTzcW0XGhTiCj_9f3c2bLS7iX7vE_Pw53jbKg",
                                    "width": 3015
                                }
                        ],
                        "place_id": "ChIJjRkT0WwFzkwRDcVNR1u452A",
                        "plus_code": {
                                "compound_code": "C8HP+Q3 Vanier, Ottawa, ON",
                                "global_code": "87Q6C8HP+Q3"
                        },
                        "rating": 4,
                        "reference": "ChIJjRkT0WwFzkwRDcVNR1u452A",
                        "scope": "GOOGLE",
                        "types": [
                                "grocery_or_supermarket",
                                "pharmacy",
                                "bakery",
                                "food",
                                "health",
                                "point_of_interest",
                                "store",
                                "establishment"
                        ],
                        "user_ratings_total": 1479,
                        "vicinity": "100 McArthur Ave., Vanier"
                    },
                    {
                        "business_status": "OPERATIONAL",
                        "geometry": {
                                "location": {
                                    "lat": 45.410486,
                                    "lng": -75.68567399999999
                                },
                                "viewport": {
                                    "northeast": {
                                            "lat": 45.41200932989271,
                                            "lng": -75.68391525
                                    },
                                    "southwest": {
                                            "lat": 45.40930967010727,
                                            "lng": -75.68741385000001
                                    }
                                }
                        },
                        "icon": "https://maps.gstatic.com/mapfiles/place_api/icons/shopping-71.png",
                        "id": "45f7270f3a5d09a6be8270e2d07e510d8672e174",
                        "name": "Loblaws",
                        "opening_hours": {
                                "open_now": True
                        },
                        "photos": [
                                {
                                    "height": 1080,
                                    "html_attributions": [
                                            "<a href=\"https://maps.google.com/maps/contrib/113689533232418076080\">Felix</a>"
                                    ],
                                    "photo_reference": "CmRaAAAAdqnykwBPBLzmQ_ZowZBPoiOpckzhBuJ0V3JhLxwes0_Uf_USdl9zz8tDn9MVUiseJrU716Gf6-l5rGg5O5yt_kOA2JiuIw68n4FIwqLUFOCQWtcj_NGh3BQsbKs09OEJEhD-1wOJgr5QFWf04WGdL7QxGhRJfLbV-UDMFvNVjExgUg0F7F85og",
                                    "width": 1920
                                }
                        ],
                        "place_id": "ChIJjfwswroFzkwRYnZID9jrRnU",
                        "plus_code": {
                                "compound_code": "C867+5P The Glebe, Ottawa, ON",
                                "global_code": "87Q6C867+5P"
                        },
                        "rating": 4,
                        "reference": "ChIJjfwswroFzkwRYnZID9jrRnU",
                        "scope": "GOOGLE",
                        "types": [
                                "grocery_or_supermarket",
                                "pharmacy",
                                "bakery",
                                "food",
                                "health",
                                "point_of_interest",
                                "store",
                                "establishment"
                        ],
                        "user_ratings_total": 1139,
                        "vicinity": "64 Isabella St, Ottawa"
                    },
                    {
                        "business_status": "OPERATIONAL",
                        "geometry": {
                                "location": {
                                    "lat": 45.4300558,
                                    "lng": -75.6834923
                                },
                                "viewport": {
                                    "northeast": {
                                            "lat": 45.43128977989273,
                                            "lng": -75.68204712010727
                                    },
                                    "southwest": {
                                            "lat": 45.42859012010728,
                                            "lng": -75.68474677989272
                                    }
                                }
                        },
                        "icon": "https://maps.gstatic.com/mapfiles/place_api/icons/pharmacy_cross-71.png",
                        "id": "27cfff6ae2907f321cfc60bc5ede69de3e00e3c3",
                        "name": "Loblaw pharmacy",
                        "opening_hours": {
                                "open_now": True
                        },
                        "place_id": "ChIJa2EA1wEFzkwR0hRNQFhyHqk",
                        "plus_code": {
                                "compound_code": "C8J8+2J Lower Town, Ottawa, ON",
                                "global_code": "87Q6C8J8+2J"
                        },
                        "rating": 3.7,
                        "reference": "ChIJa2EA1wEFzkwR0hRNQFhyHqk",
                        "scope": "GOOGLE",
                        "types": [
                                "pharmacy",
                                "health",
                                "point_of_interest",
                                "store",
                                "establishment"
                        ],
                        "user_ratings_total": 7,
                        "vicinity": "375 Rideau St, Ottawa"
                    },
                    {
                        "business_status": "OPERATIONAL",
                        "geometry": {
                                "location": {
                                    "lat": 45.39812140000001,
                                    "lng": -75.6240935
                                },
                                "viewport": {
                                    "northeast": {
                                            "lat": 45.39950077989272,
                                            "lng": -75.62251902010728
                                    },
                                    "southwest": {
                                            "lat": 45.39680112010728,
                                            "lng": -75.62521867989273
                                    }
                                }
                        },
                        "icon": "https://maps.gstatic.com/mapfiles/place_api/icons/shopping-71.png",
                        "id": "dd838982fd5812472cc4f13513d8fe7d27c7dbdc",
                        "name": "Loblaws",
                        "opening_hours": {
                                "open_now": True
                        },
                        "photos": [
                                {
                                    "height": 1080,
                                    "html_attributions": [
                                            "<a href=\"https://maps.google.com/maps/contrib/114467538196446414678\">Kevin Haratian</a>"
                                    ],
                                    "photo_reference": "CmRaAAAA2Tysupt5f2Smd4MxAoZ5TrTBB6WBGo1PcFewFAkQfbuXyHCv_b_qGwHWWOQgOR32vuu2k1Vm_RfLAnr0j57PpalIihVY2OM7Jivl6QFmmPeJnjOHiYnTWadH_S6SXr4XEhCaixbqSKjTbd5AuJUceu33GhQJuKH_sHopZy3ByNakwW_QMChONQ",
                                    "width": 1920
                                }
                        ],
                        "place_id": "ChIJr53A2RMPzkwRq_xAwtIKqrI",
                        "plus_code": {
                                "compound_code": "99XG+69 Elmvale - Eastway - Riverview - Riverview Park West, Ottawa, ON",
                                "global_code": "87Q699XG+69"
                        },
                        "rating": 3.8,
                        "reference": "ChIJr53A2RMPzkwRq_xAwtIKqrI",
                        "scope": "GOOGLE",
                        "types": [
                                "grocery_or_supermarket",
                                "pharmacy",
                                "bakery",
                                "food",
                                "health",
                                "point_of_interest",
                                "store",
                                "establishment"
                        ],
                        "user_ratings_total": 393,
                        "vicinity": "1910 St Laurent Blvd, Ottawa"
                    },
                    {
                        "business_status": "OPERATIONAL",
                        "geometry": {
                                "location": {
                                    "lat": 45.4150838,
                                    "lng": -75.696463
                                },
                                "viewport": {
                                    "northeast": {
                                            "lat": 45.41648962989272,
                                            "lng": -75.69498252010729
                                    },
                                    "southwest": {
                                            "lat": 45.41378997010728,
                                            "lng": -75.69768217989272
                                    }
                                }
                        },
                        "icon": "https://maps.gstatic.com/mapfiles/place_api/icons/pharmacy_cross-71.png",
                        "id": "0e9cf50e0170cd3cdbde868c05b306d70dd5ec77",
                        "name": "Loblaw pharmacy",
                        "opening_hours": {
                                "open_now": True
                        },
                        "photos": [
                                {
                                    "height": 2048,
                                    "html_attributions": [
                                            "<a href=\"https://maps.google.com/maps/contrib/109895037473711536718\">Nicolas P.</a>"
                                    ],
                                    "photo_reference": "CmRaAAAAtjzn_rSmTW3gKmvesUT2PYYfOwpsXxVAkyTZkV450lLtT05WxfM-gtu7CFHVQFb3XvAH3gIjHz9tvtm14TeLQEjrgBvGxyO-Meg08gYJyKC390nrm3RoZLetoGT5_ndrEhATuns4MZ9hEj_kUpvCpgLSGhQhoDMAGZMN7gvJixFszdlY78xLDw",
                                    "width": 1536
                                }
                        ],
                        "place_id": "ChIJDeZHqq0FzkwRAa9CEiyVWYk",
                        "plus_code": {
                                "compound_code": "C883+2C Centretown, Ottawa, ON",
                                "global_code": "87Q6C883+2C"
                        },
                        "rating": 4.3,
                        "reference": "ChIJDeZHqq0FzkwRAa9CEiyVWYk",
                        "scope": "GOOGLE",
                        "types": [
                                "pharmacy",
                                "health",
                                "point_of_interest",
                                "store",
                                "establishment"
                        ],
                        "user_ratings_total": 3,
                        "vicinity": "296 Bank St, Ottawa"
                    },
                    {
                        "business_status": "OPERATIONAL",
                        "geometry": {
                                "location": {
                                    "lat": 45.4293416,
                                    "lng": -75.6648604
                                },
                                "viewport": {
                                    "northeast": {
                                            "lat": 45.43092362989272,
                                            "lng": -75.66355087010727
                                    },
                                    "southwest": {
                                            "lat": 45.42822397010728,
                                            "lng": -75.66625052989272
                                    }
                                }
                        },
                        "icon": "https://maps.gstatic.com/mapfiles/place_api/icons/shopping-71.png",
                        "id": "b5a175537a2ca15f4ffb5ea30c8d19800b7534fb",
                        "name": "Theodore & Pringle Optical in Loblaws",
                        "opening_hours": {
                                "open_now": True
                        },
                        "photos": [
                                {
                                    "height": 4032,
                                    "html_attributions": [
                                            "<a href=\"https://maps.google.com/maps/contrib/117972070004495584156\">Jake Bedard</a>"
                                    ],
                                    "photo_reference": "CmRaAAAAl0wjfZlvx96eejhLtBS8Ox5jbIpd0pziJ_VwHmPRBrU3WOtujkKDGQuVpyKHPWH9F3PrwbZ0dtvfnpdHMWE3zIQ0ehxvAaX2ej0uiwvL6VNU5l902tYLBtM1I_H90bq7EhD3tG2Si0fD1Uth35rTn5ZNGhQJLJfyW09zKSBFdeyBlxuP7AyPmA",
                                    "width": 3024
                                }
                        ],
                        "place_id": "ChIJq6qqFW0FzkwRNIR6K-WrbaI",
                        "plus_code": {
                                "compound_code": "C8HP+P3 Vanier, Ottawa, ON",
                                "global_code": "87Q6C8HP+P3"
                        },
                        "rating": 5,
                        "reference": "ChIJq6qqFW0FzkwRNIR6K-WrbaI",
                        "scope": "GOOGLE",
                        "types": [
                                "health",
                                "point_of_interest",
                                "store",
                                "establishment"
                        ],
                        "user_ratings_total": 1,
                        "vicinity": "100 McArthur Ave., Vanier"
                    },
                    {
                        "business_status": "OPERATIONAL",
                        "geometry": {
                                "location": {
                                    "lat": 45.4293416,
                                    "lng": -75.6648604
                                },
                                "viewport": {
                                    "northeast": {
                                            "lat": 45.43092362989272,
                                            "lng": -75.66355087010727
                                    },
                                    "southwest": {
                                            "lat": 45.42822397010728,
                                            "lng": -75.66625052989272
                                    }
                                }
                        },
                        "icon": "https://maps.gstatic.com/mapfiles/place_api/icons/pharmacy_cross-71.png",
                        "id": "ba42a194b6d3857468ca7a4d83010b28077cb677",
                        "name": "DRUGStore Pharmacy",
                        "opening_hours": {
                                "open_now": True
                        },
                        "photos": [
                                {
                                    "height": 1080,
                                    "html_attributions": [
                                            "<a href=\"https://maps.google.com/maps/contrib/108334762826943434198\">A Google User</a>"
                                    ],
                                    "photo_reference": "CmRaAAAAhxX2UTh-dj6wfKFqmHBsgVLjZCxxHm6zNQYY4n9UgO78YWvEC_RAg51J1lBolihHsRJTu_rHkkdx8XY533dHFp0wT8DTeo__CFHbbcpmDQ5N62xV7y67KoaSc02L__ZiEhB1SBhktURs0T2sBRabk0b6GhQH8D9iOnMCdPS5IaWGoZTTYeFUZw",
                                    "width": 1920
                                }
                        ],
                        "place_id": "ChIJjRkT0WwFzkwR3RXGCguWE5I",
                        "plus_code": {
                                "compound_code": "C8HP+P3 Vanier, Ottawa, ON",
                                "global_code": "87Q6C8HP+P3"
                        },
                        "rating": 4.3,
                        "reference": "ChIJjRkT0WwFzkwR3RXGCguWE5I",
                        "scope": "GOOGLE",
                        "types": [
                                "pharmacy",
                                "health",
                                "point_of_interest",
                                "store",
                                "establishment"
                        ],
                        "user_ratings_total": 4,
                        "vicinity": "100 McArthur Ave., Vanier"
                    },
                    {
                        "business_status": "OPERATIONAL",
                        "geometry": {
                                "location": {
                                    "lat": 45.4301553,
                                    "lng": -75.6838142
                                },
                                "viewport": {
                                    "northeast": {
                                            "lat": 45.43130302989272,
                                            "lng": -75.68229807010728
                                    },
                                    "southwest": {
                                            "lat": 45.42860337010728,
                                            "lng": -75.68499772989271
                                    }
                                }
                        },
                        "icon": "https://maps.gstatic.com/mapfiles/place_api/icons/generic_business-71.png",
                        "id": "65c4cfa029c8d7b3802ccc0fb54df61a9bd4f55c",
                        "name": "Bianca Santaromita-Villa - Registered Dietitian - Nutrition Services at Loblaws",
                        "photos": [
                                {
                                    "height": 3670,
                                    "html_attributions": [
                                            "<a href=\"https://maps.google.com/maps/contrib/117902428998133220571\">A Google User</a>"
                                    ],
                                    "photo_reference": "CmRaAAAAKFZxgFKkjmn1dCcX1b0gWcVP7717NE0-4Zgt5GxYCl4pyKD6XwKCCRC--0F0URNU9428O0L2s4L4So2F1j2YxINcxxr3s4SVpElNObv1iasFpsLdy2YAdL0TU2yVeAbuEhAzeWj3txS2SUthwABmhAE2GhRN2uNbAE9TQNlJ-5RKGNJiEBD52g",
                                    "width": 5505
                                }
                        ],
                        "place_id": "ChIJ61BGmrkFzkwRnpkgzS_ytw4",
                        "plus_code": {
                                "compound_code": "C8J8+3F Lower Town, Ottawa, ON",
                                "global_code": "87Q6C8J8+3F"
                        },
                        "rating": 0,
                        "reference": "ChIJ61BGmrkFzkwRnpkgzS_ytw4",
                        "scope": "GOOGLE",
                        "types": [
                                "health",
                                "point_of_interest",
                                "establishment"
                        ],
                        "user_ratings_total": 0,
                        "vicinity": "363 Rideau St, Ottawa"
                    }
            ],
            "status": "OK"
        }
        
    MEC=(
        {
            "html_attributions": [],
            "results": [],
            "status": "ZERO_RESULTS"
        })
    MF_foodmart =(
        {
            "html_attributions": [],
            "results": [
                    {
                        "business_status": "OPERATIONAL",
                        "geometry": {
                                "location": {
                                    "lat": 45.38524169999999,
                                    "lng": -75.73267799999999
                                },
                                "viewport": {
                                    "northeast": {
                                            "lat": 45.38657197989272,
                                            "lng": -75.73114762010728
                                    },
                                    "southwest": {
                                            "lat": 45.38387232010728,
                                            "lng": -75.73384727989273
                                    }
                                }
                        },
                        "icon": "https://maps.gstatic.com/mapfiles/place_api/icons/shopping-71.png",
                        "id": "0238ca848e424c3f48f8de2d8de223ae44c68f06",
                        "name": "M F Food Mart",
                        "opening_hours": {
                                "open_now": True
                        },
                        "photos": [
                                {
                                    "height": 2988,
                                    "html_attributions": [
                                            "<a href=\"https://maps.google.com/maps/contrib/108036912491902541542\">Zubair DHK</a>"
                                    ],
                                    "photo_reference": "CmRaAAAAyy2HONvrVdOCD-JnrpTJkQQvE23miI1DZKRtd1m-LD13J3a42AuE8YHGj1l5IKww9DyOBKkWgkssq9iCcrDDlLa0fiFBvEF6gGjYx1qfTq9IuN7Zvlr9umDcyWpaOmQjEhAWAY-JLRky4K5OTNzJjFbCGhSUqgKYmlyaJ9ubCrm39F55Lph5aQ",
                                    "width": 5312
                                }
                        ],
                        "place_id": "ChIJ15s5P5wGzkwRhfL4KqD3l9U",
                        "plus_code": {
                                "compound_code": "97P8+3W Carlington, Ottawa, ON",
                                "global_code": "87Q697P8+3W"
                        },
                        "rating": 4.2,
                        "reference": "ChIJ15s5P5wGzkwRhfL4KqD3l9U",
                        "scope": "GOOGLE",
                        "types": [
                                "supermarket",
                                "grocery_or_supermarket",
                                "food",
                                "point_of_interest",
                                "store",
                                "establishment"
                        ],
                        "user_ratings_total": 95,
                        "vicinity": "850 Merivale Rd, Ottawa"
                    }
            ],
            "status": "OK"
        })
        
    walmart=(
        {
            "html_attributions": [],
            "results": [
                    {
                        "business_status": "OPERATIONAL",
                        "geometry": {
                                "location": {
                                    "lat": 45.4131465,
                                    "lng": -75.6496399
                                },
                                "viewport": {
                                    "northeast": {
                                            "lat": 45.41476587989272,
                                            "lng": -75.64839242010727
                                    },
                                    "southwest": {
                                            "lat": 45.41206622010728,
                                            "lng": -75.65109207989272
                                    }
                                }
                        },
                        "icon": "https://maps.gstatic.com/mapfiles/place_api/icons/shopping-71.png",
                        "id": "41a0f208512a76d27d4494f5056587660e5ee67e",
                        "name": "Walmart Supercentre",
                        "opening_hours": {
                                "open_now": True
                        },
                        "photos": [
                                {
                                    "height": 4032,
                                    "html_attributions": [
                                            "<a href=\"https://maps.google.com/maps/contrib/106951237136261949136\">Mohamed AG</a>"
                                    ],
                                    "photo_reference": "CmRaAAAA66kfdc-l94LyDhaoTlCQCuXXukBozgbwLI-sS5q-ifYgnzLq5WvXfBi6z2E1gfhhPmO1a7FbAWz1y3d3mi8bWHPXjmKzbNVQmImW0TP-yIdc5Cz19w5r_QRhaz4MQk9dEhBTzAEHfJkkR5ZfyxlvIHapGhQ-95I36LKOuXrnVIQWZbzIl1muKw",
                                    "width": 3024
                                }
                        ],
                        "place_id": "ChIJgwr-m4AFzkwRrOXiKNn_DN4",
                        "plus_code": {
                                "compound_code": "C972+74 Industrial Park, Ottawa, ON",
                                "global_code": "87Q6C972+74"
                        },
                        "price_level": 1,
                        "rating": 3.9,
                        "reference": "ChIJgwr-m4AFzkwRrOXiKNn_DN4",
                        "scope": "GOOGLE",
                        "types": [
                                "department_store",
                                "point_of_interest",
                                "store",
                                "establishment"
                        ],
                        "user_ratings_total": 3016,
                        "vicinity": "450 Terminal Ave, Ottawa"
                    },
                    {
                        "business_status": "OPERATIONAL",
                        "geometry": {
                                "location": {
                                    "lat": 45.3854321,
                                    "lng": -75.6800422
                                },
                                "viewport": {
                                    "northeast": {
                                            "lat": 45.38676952989272,
                                            "lng": -75.67875512010727
                                    },
                                    "southwest": {
                                            "lat": 45.38406987010728,
                                            "lng": -75.68145477989272
                                    }
                                }
                        },
                        "icon": "https://maps.gstatic.com/mapfiles/place_api/icons/shopping-71.png",
                        "id": "8706b076d62df0f28be6eb8e51528c633ff8f76c",
                        "name": "Walmart Supercentre",
                        "opening_hours": {
                                "open_now": True
                        },
                        "photos": [
                                {
                                    "height": 3000,
                                    "html_attributions": [
                                            "<a href=\"https://maps.google.com/maps/contrib/113073450595369735649\">Steve Brandon</a>"
                                    ],
                                    "photo_reference": "CmRaAAAAZxN6VBQcr3wF5i5AQW6ThpQlQyLV-7nJe6fL-c0Je2jxAtxj_pQoGN06s2zaDOdeeHv_wu-9Btsg8lUm-5m5XfLlpu-GzAyrgff2rmij0-ah-fwqP__GxQsrlewIhtfFEhB8mTihCng12hhzTUGaa5gnGhRys6ecx2aA9KIeVz8aOIYgxY6SQQ",
                                    "width": 4000
                                }
                        ],
                        "place_id": "ChIJR0673DeWuEwRh8QoQz0MCto",
                        "plus_code": {
                                "compound_code": "98P9+5X Alta Vista, Ottawa, ON",
                                "global_code": "87Q698P9+5X"
                        },
                        "price_level": 1,
                        "rating": 4,
                        "reference": "ChIJR0673DeWuEwRh8QoQz0MCto",
                        "scope": "GOOGLE",
                        "types": [
                                "department_store",
                                "point_of_interest",
                                "store",
                                "establishment"
                        ],
                        "user_ratings_total": 1221,
                        "vicinity": "2277 Riverside Dr., Ottawa"
                    },
                    {
                        "business_status": "OPERATIONAL",
                        "geometry": {
                                "location": {
                                    "lat": 45.4456609,
                                    "lng": -75.7340534
                                },
                                "viewport": {
                                    "northeast": {
                                            "lat": 45.44700842989272,
                                            "lng": -75.73234987010727
                                    },
                                    "southwest": {
                                            "lat": 45.44430877010728,
                                            "lng": -75.7350495298927
                                    }
                                }
                        },
                        "icon": "https://maps.gstatic.com/mapfiles/place_api/icons/shopping-71.png",
                        "id": "22501f94fa456b2575dc430997c2d361a571785a",
                        "name": "Walmart Supercentre",
                        "opening_hours": {
                                "open_now": True
                        },
                        "photos": [
                                {
                                    "height": 2160,
                                    "html_attributions": [
                                            "<a href=\"https://maps.google.com/maps/contrib/112042016934804267825\">Fr\u00e9d\u00e9rik Boisvert</a>"
                                    ],
                                    "photo_reference": "CmRaAAAAnM_-ancXzMh51IntRpXz2iGAQUYOtxFX9xI9ydgai9-ahdDyqxXu2tIYxM0PE6S5Q0YCmulcmlwAAab5VL9PkL1z5ajPwKoefsIbBavHOkRsF0ds8d1Cv-JT-7PI5QckEhCwBYiXlVqSqB00fyqNGncbGhQrskSjacmaZym8LFIDeama2ROSaw",
                                    "width": 3840
                                }
                        ],
                        "place_id": "ChIJlQArxth3hlQRbd5GwxkEtdU",
                        "plus_code": {
                                "compound_code": "C7W8+79 Gatineau, Quebec",
                                "global_code": "87Q6C7W8+79"
                        },
                        "price_level": 1,
                        "rating": 3.8,
                        "reference": "ChIJlQArxth3hlQRbd5GwxkEtdU",
                        "scope": "GOOGLE",
                        "types": [
                                "department_store",
                                "point_of_interest",
                                "store",
                                "establishment"
                        ],
                        "user_ratings_total": 2410,
                        "vicinity": "425 Boulevard Saint-Joseph #1, Gatineau"
                    },
                    {
                        "business_status": "OPERATIONAL",
                        "geometry": {
                                "location": {
                                    "lat": 45.4647976,
                                    "lng": -75.7205005
                                },
                                "viewport": {
                                    "northeast": {
                                            "lat": 45.46619272989272,
                                            "lng": -75.71846215
                                    },
                                    "southwest": {
                                            "lat": 45.46349307010728,
                                            "lng": -75.72117995
                                    }
                                }
                        },
                        "icon": "https://maps.gstatic.com/mapfiles/place_api/icons/shopping-71.png",
                        "id": "356556f3e349bd3ea328d5b9ee097f34fc1647e4",
                        "name": "Walmart Supercentre",
                        "opening_hours": {
                                "open_now": True
                        },
                        "photos": [
                                {
                                    "height": 2603,
                                    "html_attributions": [
                                            "<a href=\"https://maps.google.com/maps/contrib/113073450595369735649\">Steve Brandon</a>"
                                    ],
                                    "photo_reference": "CmRaAAAAiYGuXcZAHlRKGsu6Ns1Xtc5h_xVgwkLYOyzaMDsHtumncJy0ODc-m_ZDueFyGLzJHUP904EsV-i7s5bwv69iD8y3M6QET7DORqYxfjfipl8-DbmEkDh5yOxOdGNLqASbEhA8Y9006S03SnpqE1uYm8YGGhSPT59KTZfYTRsGXLmp_IpYjMyxmA",
                                    "width": 3470
                                }
                        ],
                        "place_id": "ChIJhZr7eEIbzkwR-ILYPRl1gjU",
                        "plus_code": {
                                "compound_code": "F77H+WQ Gatineau, Quebec",
                                "global_code": "87Q6F77H+WQ"
                        },
                        "price_level": 1,
                        "rating": 3.9,
                        "reference": "ChIJhZr7eEIbzkwR-ILYPRl1gjU",
                        "scope": "GOOGLE",
                        "types": [
                                "department_store",
                                "point_of_interest",
                                "store",
                                "establishment"
                        ],
                        "user_ratings_total": 3424,
                        "vicinity": "51 De La Gappe Blvd, Gatineau"
                    },
                    {
                        "business_status": "OPERATIONAL",
                        "geometry": {
                                "location": {
                                    "lat": 45.3854621,
                                    "lng": -75.67997190000001
                                },
                                "viewport": {
                                    "northeast": {
                                            "lat": 45.38703557989272,
                                            "lng": -75.67645875
                                    },
                                    "southwest": {
                                            "lat": 45.38433592010728,
                                            "lng": -75.68114295000002
                                    }
                                }
                        },
                        "icon": "https://maps.gstatic.com/mapfiles/place_api/icons/shopping-71.png",
                        "id": "48e7fe868e7c7d2c7e4727e8ac39b5ad1a2cd00c",
                        "name": "Walmart Grocery Pickup",
                        "opening_hours": {
                                "open_now": True
                        },
                        "photos": [
                                {
                                    "height": 4912,
                                    "html_attributions": [
                                            "<a href=\"https://maps.google.com/maps/contrib/115221351913086359303\">A Google User</a>"
                                    ],
                                    "photo_reference": "CmRaAAAALud5LBHMhs_TQbkGqLzIgBJ-HeXZc-__YAktTS-z7fmLtTd1GIQ7LxC8cc4cOqtkZX-Z0MH3NuHiFV7ipoDFmZ18gfhpEsVjE9MpSXmeNvQ8bwV5UKg_3mb3MwOkyKeJEhC9oXpoFcunh4wgTtKe72N1GhREEfc-L4OyGFK7w9mX4aD4xTFX_A",
                                    "width": 6221
                                }
                        ],
                        "place_id": "ChIJB0kFGsEFzkwRn2UF2U8-D1Q",
                        "plus_code": {
                                "compound_code": "98PC+52 Alta Vista, Ottawa, ON",
                                "global_code": "87Q698PC+52"
                        },
                        "rating": 0,
                        "reference": "ChIJB0kFGsEFzkwRn2UF2U8-D1Q",
                        "scope": "GOOGLE",
                        "types": [
                                "grocery_or_supermarket",
                                "bakery",
                                "food",
                                "health",
                                "point_of_interest",
                                "store",
                                "establishment"
                        ],
                        "user_ratings_total": 0,
                        "vicinity": "2277 Riverside Dr., Ottawa"
                    },
                    {
                        "business_status": "OPERATIONAL",
                        "geometry": {
                                "location": {
                                    "lat": 45.4131465,
                                    "lng": -75.6496399
                                },
                                "viewport": {
                                    "northeast": {
                                            "lat": 45.41476142989271,
                                            "lng": -75.64844017010728
                                    },
                                    "southwest": {
                                            "lat": 45.41206177010727,
                                            "lng": -75.65113982989271
                                    }
                                }
                        },
                        "icon": "https://maps.gstatic.com/mapfiles/place_api/icons/pharmacy_cross-71.png",
                        "id": "b2e39c73cc04d24a7a2cf08c8271758ea26fb0bb",
                        "name": "Walmart Pharmacy",
                        "opening_hours": {
                                "open_now": True
                        },
                        "place_id": "ChIJL3Iqm4AFzkwRSD0HwQsNzsg",
                        "plus_code": {
                                "compound_code": "C972+74 Industrial Park, Ottawa, ON",
                                "global_code": "87Q6C972+74"
                        },
                        "price_level": 1,
                        "rating": 4.3,
                        "reference": "ChIJL3Iqm4AFzkwRSD0HwQsNzsg",
                        "scope": "GOOGLE",
                        "types": [
                                "pharmacy",
                                "health",
                                "point_of_interest",
                                "store",
                                "establishment"
                        ],
                        "user_ratings_total": 12,
                        "vicinity": "450 Terminal Ave, Ottawa"
                    },
                    {
                        "business_status": "OPERATIONAL",
                        "geometry": {
                                "location": {
                                    "lat": 45.4456111,
                                    "lng": -75.73388349999999
                                },
                                "viewport": {
                                    "northeast": {
                                            "lat": 45.44695917989272,
                                            "lng": -75.73226522010728
                                    },
                                    "southwest": {
                                            "lat": 45.44425952010728,
                                            "lng": -75.73496487989273
                                    }
                                }
                        },
                        "icon": "https://maps.gstatic.com/mapfiles/place_api/icons/pharmacy_cross-71.png",
                        "id": "97d709a2c3d9a4c58acab5c6eb6e53398cbd3fff",
                        "name": "Walmart Pharmacy",
                        "opening_hours": {
                                "open_now": True
                        },
                        "place_id": "ChIJr7rIv58EzkwRkFILoeNxMXg",
                        "plus_code": {
                                "compound_code": "C7W8+6C Gatineau, Quebec",
                                "global_code": "87Q6C7W8+6C"
                        },
                        "price_level": 1,
                        "rating": 3.8,
                        "reference": "ChIJr7rIv58EzkwRkFILoeNxMXg",
                        "scope": "GOOGLE",
                        "types": [
                                "pharmacy",
                                "health",
                                "point_of_interest",
                                "store",
                                "establishment"
                        ],
                        "user_ratings_total": 4,
                        "vicinity": "425 Boulevard Saint-Joseph, Gatineau"
                    },
                    {
                        "business_status": "OPERATIONAL",
                        "geometry": {
                                "location": {
                                    "lat": 45.4647352,
                                    "lng": -75.7201769
                                },
                                "viewport": {
                                    "northeast": {
                                            "lat": 45.46622037989272,
                                            "lng": -75.71838902010728
                                    },
                                    "southwest": {
                                            "lat": 45.46352072010728,
                                            "lng": -75.72108867989272
                                    }
                                }
                        },
                        "icon": "https://maps.gstatic.com/mapfiles/place_api/icons/pharmacy_cross-71.png",
                        "id": "13bb03a053731a61291601155e1ec7483172367d",
                        "name": "Walmart Pharmacy",
                        "opening_hours": {
                                "open_now": True
                        },
                        "place_id": "ChIJhbpQu1QbzkwRdCq3Bz7v9qY",
                        "plus_code": {
                                "compound_code": "F77H+VW Gatineau, Quebec",
                                "global_code": "87Q6F77H+VW"
                        },
                        "price_level": 1,
                        "rating": 3.3,
                        "reference": "ChIJhbpQu1QbzkwRdCq3Bz7v9qY",
                        "scope": "GOOGLE",
                        "types": [
                                "pharmacy",
                                "health",
                                "point_of_interest",
                                "store",
                                "establishment"
                        ],
                        "user_ratings_total": 3,
                        "vicinity": "51 Boulevard de la Gappe, Gatineau"
                    },
                    {
                        "business_status": "OPERATIONAL",
                        "geometry": {
                                "location": {
                                    "lat": 45.4652114,
                                    "lng": -75.7197547
                                },
                                "viewport": {
                                    "northeast": {
                                            "lat": 45.46659202989272,
                                            "lng": -75.71835857010727
                                    },
                                    "southwest": {
                                            "lat": 45.46389237010728,
                                            "lng": -75.72105822989272
                                    }
                                }
                        },
                        "icon": "https://maps.gstatic.com/mapfiles/place_api/icons/pharmacy_cross-71.png",
                        "id": "f5c9213cd2b658fe14ff7728cc4cff66a60432a4",
                        "name": "Walmart Pharmacy",
                        "opening_hours": {
                                "open_now": True
                        },
                        "place_id": "ChIJ95WmoVQbzkwRr7kyNH3eKPc",
                        "plus_code": {
                                "compound_code": "F78J+33 Gatineau, Quebec",
                                "global_code": "87Q6F78J+33"
                        },
                        "price_level": 1,
                        "rating": 0,
                        "reference": "ChIJ95WmoVQbzkwRr7kyNH3eKPc",
                        "scope": "GOOGLE",
                        "types": [
                                "pharmacy",
                                "health",
                                "point_of_interest",
                                "store",
                                "establishment"
                        ],
                        "user_ratings_total": 0,
                        "vicinity": "51 Boulevard de la Gappe, Gatineau"
                    },
                    {
                        "business_status": "OPERATIONAL",
                        "geometry": {
                                "location": {
                                    "lat": 45.4131685,
                                    "lng": -75.6495735
                                },
                                "viewport": {
                                    "northeast": {
                                            "lat": 45.41478482989272,
                                            "lng": -75.64827402010728
                                    },
                                    "southwest": {
                                            "lat": 45.41208517010728,
                                            "lng": -75.65097367989273
                                    }
                                }
                        },
                        "icon": "https://maps.gstatic.com/mapfiles/place_api/icons/shopping-71.png",
                        "id": "738e72eb894734cc4e2ce36161cd1308c8aa7a1b",
                        "name": "Walmart Tire & Lube Express",
                        "opening_hours": {
                                "open_now": True
                        },
                        "place_id": "ChIJPyZomYAFzkwRDbckGIWq6OY",
                        "plus_code": {
                                "compound_code": "C972+75 Industrial Park, Ottawa, ON",
                                "global_code": "87Q6C972+75"
                        },
                        "price_level": 1,
                        "rating": 2.6,
                        "reference": "ChIJPyZomYAFzkwRDbckGIWq6OY",
                        "scope": "GOOGLE",
                        "types": [
                                "car_repair",
                                "point_of_interest",
                                "store",
                                "establishment"
                        ],
                        "user_ratings_total": 7,
                        "vicinity": "450 Terminal Ave, Ottawa"
                    },
                    {
                        "business_status": "OPERATIONAL",
                        "geometry": {
                                "location": {
                                    "lat": 45.4456609,
                                    "lng": -75.7340534
                                },
                                "viewport": {
                                    "northeast": {
                                            "lat": 45.44701072989272,
                                            "lng": -75.73270357010728
                                    },
                                    "southwest": {
                                            "lat": 45.44431107010728,
                                            "lng": -75.73540322989273
                                    }
                                }
                        },
                        "icon": "https://maps.gstatic.com/mapfiles/place_api/icons/shopping-71.png",
                        "id": "1da332cf63cab53a4287878f2126a73b38728f65",
                        "name": "Walmart Photo Center",
                        "opening_hours": {
                                "open_now": True
                        },
                        "place_id": "ChIJl4YLT2oFzkwRbD_oT4u4Zdc",
                        "plus_code": {
                                "compound_code": "C7W8+79 Gatineau, Quebec",
                                "global_code": "87Q6C7W8+79"
                        },
                        "rating": 0,
                        "reference": "ChIJl4YLT2oFzkwRbD_oT4u4Zdc",
                        "scope": "GOOGLE",
                        "types": [
                                "electronics_store",
                                "home_goods_store",
                                "point_of_interest",
                                "store",
                                "establishment"
                        ],
                        "user_ratings_total": 0,
                        "vicinity": "425 Boulevard Saint-Joseph #1, Gatineau"
                    },
                    {
                        "business_status": "OPERATIONAL",
                        "geometry": {
                                "location": {
                                    "lat": 45.3856281,
                                    "lng": -75.6774777
                                },
                                "viewport": {
                                    "northeast": {
                                            "lat": 45.38697792989272,
                                            "lng": -75.67612787010728
                                    },
                                    "southwest": {
                                            "lat": 45.38427827010728,
                                            "lng": -75.67882752989271
                                    }
                                }
                        },
                        "icon": "https://maps.gstatic.com/mapfiles/place_api/icons/pharmacy_cross-71.png",
                        "id": "36ea2edea4f389c6b3b36b2f5c59b9fdc1533643",
                        "name": "Walmart Pharmacy",
                        "opening_hours": {
                                "open_now": True
                        },
                        "place_id": "ChIJkyA958MFzkwRU7g06xvTapo",
                        "plus_code": {
                                "compound_code": "98PF+72 Alta Vista, Ottawa, ON",
                                "global_code": "87Q698PF+72"
                        },
                        "rating": 4.5,
                        "reference": "ChIJkyA958MFzkwRU7g06xvTapo",
                        "scope": "GOOGLE",
                        "types": [
                                "pharmacy",
                                "health",
                                "point_of_interest",
                                "store",
                                "establishment"
                        ],
                        "user_ratings_total": 4,
                        "vicinity": "2277 Riverside Dr., Ottawa"
                    },
                    {
                        "business_status": "OPERATIONAL",
                        "geometry": {
                                "location": {
                                    "lat": 45.4647976,
                                    "lng": -75.7205005
                                },
                                "viewport": {
                                    "northeast": {
                                            "lat": 45.46614742989271,
                                            "lng": -75.71915067010728
                                    },
                                    "southwest": {
                                            "lat": 45.46344777010727,
                                            "lng": -75.72185032989273
                                    }
                                }
                        },
                        "icon": "https://maps.gstatic.com/mapfiles/place_api/icons/shopping-71.png",
                        "id": "af0d456657b5a5d0545110b5078a53a5005d2966",
                        "name": "Walmart Photo Center",
                        "place_id": "ChIJb7o-LwgbzkwRynQNoFk7OxY",
                        "plus_code": {
                                "compound_code": "F77H+WQ Gatineau, Quebec",
                                "global_code": "87Q6F77H+WQ"
                        },
                        "rating": 0,
                        "reference": "ChIJb7o-LwgbzkwRynQNoFk7OxY",
                        "scope": "GOOGLE",
                        "types": [
                                "electronics_store",
                                "home_goods_store",
                                "point_of_interest",
                                "store",
                                "establishment"
                        ],
                        "user_ratings_total": 0,
                        "vicinity": "51 Boulevard de la Gappe, Gatineau"
                    }
            ],
        "status": "OK"
        })
    
def get_nearby_response_False():
    return {
            "html_attributions": [],
            "results": [],
            "status": "ZERO_RESULTS"
        }

#-------------------------------CHECK IF A SAVED STORE FUNCTION---------------------------------------------------#
def check_inside(ul,sl):

    check_ary=[]

    if ul[3]>sl[1] or ul[1]<sl[3]:
        check_ary.append(False)
    else:
        check_ary.append(True)
    
    if ul[2]>sl[0] or ul[0]<sl[2]:
        check_ary.append(False)
    else:
        check_ary.append(True)

    if False in check_ary:
        inside = False
    else:
        inside = True
    print
    return inside
def search_nearby(ul,kw):
    '''
    Notes:
        inputs:
            ul =user location 
            kw= keywords for location of the product puschase
            condition = 'true'/'false'- for testing this will be removed for application

       if the user is whitin a certain range of the location 
        outputs:
        store_peramete=[a,b,c,d]
         note: a,b,c,d are the lng and lat values of the stores parameter
         
       *NOTE: for testing purpose we are taking in a conditon 
              if condition = true, the mock api will out put result
              else  condition = 'false',  the mock api will ouput 0 result
              
        '''
    userlocation = ul
    keyword = kw

    #'''-remove when using actual url response                           **

    API_key = 'AIzaSyB4BdrazYRTttzy6H5XAu6ib7uL87bvgjk'

    request_url ='https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={lat},{lng}&radius=5000&keyword={key}&key={API}'.format(lat=userlocation[0],lng=userlocation[1],key=keyword,API=API_key)
    nearby_request = urllib.request.urlopen(request_url).read()
    nearby_response=json.loads(nearby_request)
    #remove when using actual url response-'''
    
    
    '''
    # Note: 
    #       nearby_response_true and nearby_response_false were tested and are actual response from url get reuqest
    if condotion==True:
        nearby_response=get_nearby_response_true(keyword)
    else:
        nearby_response=get_nearby_response_False()
    '''
    if nearby_response['status']=="OK":
        store_perameter=[
        nearby_response['results'][0]["geometry"]['viewport']["northeast"]['lat'],
        nearby_response['results'][0]["geometry"]['viewport']["northeast"]['lng'],
        nearby_response['results'][0]["geometry"]['viewport']["southwest"]['lat'],
        nearby_response['results'][0]["geometry"]['viewport']["southwest"]['lng']
        ]
        rng=0.0001169
        user_location_range=[userlocation[0]-rng,userlocation[1]+rng,userlocation[0]+rng,userlocation[1]-rng]

        response=check_inside(user_location_range,store_perameter)
        if response == True:
            return response
    else:
        print('not near a store')
#-------------------------------SQL CODE TO BRING LIST OF SaVED LOCATIONS---------------------------------------------------#
def query_places(u_id,connection):
        user_id=u_id 
        query = f"SELECT count(*) item_name FROM saved_items WHERE user_id = '{user_id}'"
        location_query= f"SELECT DISTINCT purchase_location FROM saved_items WHERE user_id = '{user_id}'"

        return_text=execute_read_query(connection, query)
        loc_list=[]

        if return_text[0][0]>0:
            loc_query_resp=execute_read_query(connection, location_query)
            for x in range(0,len(loc_query_resp)):
                loc_list.append(loc_query_resp[x][0])
            return loc_list

        else:
            pass
#-------------------------------PRINT SAVED ITEM AT GIVEN STORE FUNCTION---------------------------------------------------#
def print_items(u_id,u_n,loc):

        user_id= u_id
        location = loc
        name= u_n

        #because of the "@" in the email PostgreSQL the query doesnt work so the email is entered as a string thus adding extra quotation marks 
        query = f"SELECT count(*) item_name FROM saved_items WHERE user_id = '{user_id}' and purchase_location ='{location}'"

        item_query= f"SELECT item_name  FROM saved_items WHERE user_id = '{user_id}' and purchase_location ='{location}'"

        return_text=execute_read_query(connection, query)

        if return_text[0][0]>0:
            item=execute_read_query(connection, item_query)

            print(f'Hi! {name}, you are in {location}')
            print('you wated to purchase the following item: ')
            for x in range(0,len(item)):
                print(' * '+ item[x][0])

        else:
            pass

#---------------------------------------CODE SECTION:-------------------------------------------------#

#--------------------------------------LOGIN SECTION-------------------------------------------------#
login_status = False
while login_status == False:
    
    newuser =input('New Member? y/n:  ')
    if newuser == 'y':
        #user inputs:
        username= input('Name?')
        useremail= email_verification(connection)
        password=password_check()

        #calling function above to add data to the table:
        add_data_registration(username,useremail,password,connection)

        newuser=='n'
    else:
        userdetail=login_verification(connection)
        login_status = True

user_id=userdetail[0]
user_name=userdetail[1]
#--------------------------------------SAVE NEW ITEM-------------------------------------------------#
save_new_item(user_id,connection)

#--------------------------------------USER LOCATION-------------------------------------------------#
location_accurate= False
while location_accurate == False:
    userlocation = get_user_location()
    location_accuracy=userlocation[2]
    if location_accuracy<10000:
        location_accurate = True
#--------------------------------------LOCATION QUERY AND PRINT-------------------------------------------------#
location_saved=query_places(user_id,connection)


#test_condition =[True,False,False,False]

for x in range(0,len(location_saved)):

    check_store_nearby_parameter=search_nearby(userlocation,location_saved[x].replace(" ", "_")) 
    #python doesnt execute URL search with empty space inside so replacng ' ' by '_'
    
    if check_store_nearby_parameter == True:
        print_items(user_id,user_name,location_saved[x])


    