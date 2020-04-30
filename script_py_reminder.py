
import requests
import urllib.request
import json
'''
    stores_type is mock api for testing, in future this will be 
    converted into a google place search/ type API.#the api would be 
    modified so that the library can be brodened.

    Note:
    
        person_saved_item is a dictionary for all the items stored by the user,
        keys are the user names and the purchase items are saved as a list

        * figure out a way tosave it in json format
'''
#persoal items are the saved user input
personal_item ={
    'rafida9@gmail.com': 
    #rafida9@gmail.com is the username
    
    #the following are the items saved by the user
        [
            {'item':'black berry',
            'where':'walmart'},
        
            {'item':'eggs',
            'where':'walmart'},
        
            {'item':'Pc Chocolate',
            'where':'loblaws'},
        
            {'item':'fries',
            'where':'mcdonalds'},
        
            {'item':'mouse',
            'where':'electronics_store'} 
    ]
}
'''
will be used for multiple user testing:  

         'kath.443@hotmail.com':

         [{'name':'tea','where':'grocery store'}
          ,{'name':'milk','where':'grocery store'}
          ,{'name':'pill','where':'pharmacy'}
          ,{'name':'battery','where':'electronic store'} ]}
          
'''

#list of different types of places within google library

list_of_type_of_store=[
                    'airport',
                    'amusement_park',
                    'aquarium',
                    'art_gallery',
                    'atm',
                    'bakery',
                    'bank',
                    'bar',
                    'beauty_salon',
                    'bicycle_store',
                    'book_store',
                    'bowling_alley',
                    'bus_station',
                    'cafe',
                    'campground',
                    'car_dealer',
                    'car_rental',
                    'car_repair',
                    'car_wash',
                    'casino',
                    'cemetery',
                    'church',
                    'city_hall',
                    'clothing_store',
                    'convenience_store',
                    'courthouse',
                    'dentist',
                    'department_store',
                    'doctor',
                    'drugstore',
                    'electrician',
                    'electronics_store',
                    'embassy',
                    'fire_station',
                    'florist',
                    'funeral_home',
                    'furniture_store',
                    'gas_station',
                    'grocery_or_supermarket',
                    'gym',
                    'hair_care',
                    'hardware_store',
                    'hindu_temple',
                    'home_goods_store',
                    'hospital',
                    'insurance_agency',
                    'jewelry_store',
                    'laundry',
                    'lawyer',
                    'library',
                    'light_rail_station',
                    'liquor_store',
                    'local_government_office',
                    'locksmith',
                    'lodging',
                    'meal_delivery',
                    'meal_takeaway',
                    'mosque',
                    'movie_rental',
                    'movie_theater',
                    'moving_company',
                    'museum',
                    'night_club',
                    'painter',
                    'park',
                    'parking',
                    'pet_store',
                    'pharmacy',
                    'physiotherapist',
                    'plumber',
                    'police',
                    'post_office',
                    'primary_school',
                    'real_estate_agency',
                    'restaurant',
                    'roofing_contractor',
                    'rv_park',
                    'school',
                    'secondary_school',
                    'shoe_store',
                    'shopping_mall',
                    'spa',
                    'stadium',
                    'storage',
                    'store',
                    'subway_station',
                    'supermarket',
                    'synagogue',
                    'taxi_stand',
                    'tourist_attraction',
                    'train_station',
                    'transit_station',
                    'travel_agency',
                    'university',
                    'veterinary_care',
                    'zoo'
                    ]
username= 'rafida9@gmail.com'

def type_keyword_sorting(username,personal_item):

    ''' This function takes in the username and his personal item list to sort the users
    stored item into a list of key words and type
        the inputs are as following:
            type_keyword_sorting(username,personal_item)
            * username: is a string
            * personal_item: dictionary of saved item for the user
        output:
            a list [ary_keywords,ary_type]
    '''

    ary_keywords=[]
    ary_type=[]

    for x in range(0,len(personal_item[username])):

        if personal_item[username][x]['where'] in list_of_type_of_store:

            ary_type.append(personal_item[username][x]['where'])
        else:
            ary_keywords.append(personal_item[username][x]['where'])

    sorted_list=[ary_keywords,ary_type]

    return sorted_list

sorted=type_keyword_sorting(username,personal_item)


#the code below works making it a comment because do not want to continuously call on google API and be charged
'''def get_user_location():

    ''uses the google url post to get users location''

    url_requested= 'https://www.googleapis.com/geolocation/v1/geolocate?key=AIzaSyB4BdrazYRTttzy6H5XAu6ib7uL87bvgjk'
    response = requests.post( url_requested)
    r=response.text
    x=json.loads(r)
    lat=x['location']['lat']
    lng=x['location']['lng']
    accu=x['accuracy']
    user_location=[lat,lng,accu]

    return user_location'''

#userlocation = get_user_location()

userlocation = [45.4279636, -75.6834408, 1062]

#below is an example of search for searching walmart near me

'''inputs were:

userlocation = [longitudonal, lattitude, 1062]
keyword = the place where the item is saved for the user
API_key = generated by google API

url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location='+userlocation[0] ,userlocation[1]+'&radius=500&keyword=' keyword '&key='+ api_key
'''


#the following is an example for searching for a place near the user:

#userlocation = [longitudonal, lattitude, 1062]
#keyword = sorted[0][0] = walmart
#API_key = AIzaSyB4BdrazYRTttzy6H5XAu6ib7uL87bvgjk

# request_url ='https://maps.googleapis.com/maps/api/place/nearbysearch/json?
#               location={loc},{lat}&radius=500&keyword={key}&key={API}'.format(loc=userlocation[0],lat=userlocation[1],key=keyword,API=API_key)
#nearby_request = urllib.request.urlopen(request_url).read()
#nearby_response=json.loads(nearby_request)


#follwoing is the function for searching for for given keyword:

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
         
    # the following code will be used to GET response from google API
    '''userlocation = ul
    keyword = kw
    API_key = 'AIzaSyB4BdrazYRTttzy6H5XAu6ib7uL87bvgjk'

    request_url ='https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={lng},{lat}&radius=500&keyword={key}&key={API}'.format(lng=userlocation[0],lat=userlocation[1],key=keyword,API=API_key)
    nearby_request = urllib.request.urlopen(request_url).read()
    nearby_response=json.loads(nearby_request)'''   
    #the following was the response when there IS A RESULTS in provided perameters
    nearby_response_true ={
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

    #the following was the response when there IS NO RESULTS in provided perameters
    nearby_response_false={
            "html_attributions": [],
            "results": [],
            "status": "ZERO_RESULTS"
        }
    # Note: 
    #       nearby_response_true and nearby_response_false were tested and are actual response from url get reuqest
    if condotion=='true':
        nearby_response=nearby_response_true
    else:
        nearby_response=nearby_response_false
    if nearby_response['status']=="OK":
        store_perameter=[
        nearby_response_true['results'][0]["geometry"]['viewport']["northeast"]['lat'],
        nearby_response_true['results'][0]["geometry"]['viewport']["northeast"]['lng'],
        nearby_response_true['results'][0]["geometry"]['viewport']["southwest"]['lat'],
        nearby_response_true['results'][0]["geometry"]['viewport']["southwest"]['lng']
        ]
        return store_perameter


test_store_nearby_parameter=search_nearby(userlocation,'walmart','true')



#the perameters of the users location range will be to 0.0001169 degrees 
'''
NOTE:
    13/111200=0.0001169 where 13 is the highest uncetanity in a cell phone gps from in an urban environment
    'Smartphone GPS accuracy study in an urban environment'-Krista Merry, Pete Bettinger
'''
rng=0.0001169

user_location_range=[userlocation[0]-rng,userlocation[1]+rng,userlocation[0]+rng,userlocation[1]-rng]
print(user_location_range)
print(test_store_nearby_parameter)


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

    if check_ary==[True,True]:
        inside = True
    else:
        inside = False
    print
    return inside


user_inside_store = check_inside(user_location_range,test_store_nearby_parameter)

if user_inside_store == True:

    print ('user inside the store')

else:

    print ('user not inside the store')




