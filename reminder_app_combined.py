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

    url_requested= 'https://www.googleapis.com/geolocation/v1/geolocate?key=INSERT GOOGLE API KEY'
    response = requests.post( url_requested)
    r=response.text
    x=json.loads(r)
    lat=x['location']['lat']
    lng=x['location']['lng']
    accu=x['accuracy']
    user_location=[lat,lng,accu]
    '''
    #for test purposes:
    user_location= [45.4131465, -75.6496399, 13]
    return user_location
#-------------------------------CHECK INSIDE STORE FUNCTION---------------------------------------------------#
# mock api result
def get_nearby_response_true():
    return {
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
                    "open_now": 'false'
                },
                "photos": [
                    {
                        "height": 4032,
                        "html_attributions": [
                            "<a href=\"https://maps.google.com/maps/contrib/106951237136261949136\">Mohamed AG</a>"
                        ],
                        "photo_reference": "CmRaAAAAfP-cR0-ugTCk6gEKs57xeURC8ryfbwxMl8grPLlNpIr0_vFusSoziBpNqJ-rWYHsx-SBI9p66EG25tQ_oJTqjYuhuSf68WNfiFms8HY2TYmC6OMXzbsv5KYeFbgqqo8qEhCarE-nr-hzBVnw4gKdmx0OGhSKaiVm9h0D-uLCK8encQ2Tx4-oOQ",
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
                "user_ratings_total": 3012,
                "vicinity": "450 Terminal Ave, Ottawa"
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
                    "open_now": 'false'
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
                        "lat": 45.413571,
                        "lng": -75.65024830000002
                    },
                    "viewport": {
                        "northeast": {
                            "lat": 45.41495867989273,
                            "lng": -75.64890562010727
                        },
                        "southwest": {
                            "lat": 45.41225902010729,
                            "lng": -75.65160527989272
                        }
                    }
                },
                "icon": "https://maps.gstatic.com/mapfiles/place_api/icons/shopping-71.png",
                "id": "c77562c6593774c16dfe4c9dcdf77f6d6d78efc8",
                "name": "Vision Center At Walmart",
                "place_id": "ChIJL3Iqm4AFzkwRCgewCTgTmBk",
                "plus_code": {
                    "compound_code": "C87X+CW Industrial Park, Ottawa, ON",
                    "global_code": "87Q6C87X+CW"
                },
                "price_level": 1,
                "rating": 2.6,
                "reference": "ChIJL3Iqm4AFzkwRCgewCTgTmBk",
                "scope": "GOOGLE",
                "types": [
                    "health",
                    "point_of_interest",
                    "store",
                    "establishment"
                ],
                "user_ratings_total": 5,
                "vicinity": "450 Terminal Ave, Ottawa"
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
                            "lat": 45.41477142989272,
                            "lng": -75.64833287010727
                        },
                        "southwest": {
                            "lat": 45.41207177010727,
                            "lng": -75.65103252989272
                        }
                    }
                },
                "icon": "https://maps.gstatic.com/mapfiles/place_api/icons/shopping-71.png",
                "id": "a66bafefe2a671580f27a0100717771da2405013",
                "name": "Walmart Grocery Pickup",
                "opening_hours": {
                    "open_now": 'false'
                },
                "place_id": "ChIJ0V2YJjkFzkwR8O9CLvvP22U",
                "plus_code": {
                    "compound_code": "C972+74 Industrial Park, Ottawa, ON",
                    "global_code": "87Q6C972+74"
                },
                "rating": 0,
                "reference": "ChIJ0V2YJjkFzkwR8O9CLvvP22U",
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
                "vicinity": "450 Terminal Ave, Ottawa"
            }
        ],
        "status": "OK"
    }

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
def search_nearby(ul,kw,condotion):
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

    '''-remove when using actual url response                           **

    API_key = '*****************'

    request_url ='https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={lng},{lat}&radius=500&keyword={key}&key={API}'.format(lng=userlocation[0],lat=userlocation[1],key=keyword,API=API_key)
    nearby_request = urllib.request.urlopen(request_url).read()
    nearby_response=json.loads(nearby_request)

    remove when using actual url response-'''

    # Note: 
    #       nearby_response_true and nearby_response_false were tested and are actual response from url get reuqest
    if condotion==True:
        nearby_response=get_nearby_response_true()
    else:
        nearby_response=get_nearby_response_False()

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
    if location_accuracy<15:
        location_accurate = True
#--------------------------------------LOCATION QUERY AND PRINT-------------------------------------------------#
location_saved=query_places(user_id,connection)
print(len(location_saved))
print(location_saved)

test_condition =[True,False,False,False]

for x in range(0,len(location_saved)):
    check_store_nearby_parameter=search_nearby(userlocation,location_saved[x],test_condition[x])
    if check_store_nearby_parameter == True:
        print_items(user_id,user_name,location_saved[x])


    