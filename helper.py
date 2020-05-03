
def get_personal_items():
    return {
        'rafida9@gmail.com': [
                {
                    'item':'black berry',
                    'where':'walmart'
                },
            
                {
                    'item':'eggs',
                    'where':'walmart'
                },
            
                {
                    'item':'Pc Chocolate',
                    'where':'loblaws'
                },
            
                {
                    'item':'fries',
                    'where':'mcdonalds'
                },
            
                {
                    'item':'mouse',
                    'where':'electronics_store'
                } 
        ],
        'kath.443@hotmail.com': [
            {
                'item':'tea',
                'where':'grocery store'
            },
            {
                'item':'milk',
                'where':'grocery store'
            },
            {
                'item':'pill',
                'where':'pharmacy'
            },
            {
                'item':'battery',
                'where':'electronic store'
            } 
        ]
    }

def get_type_of_store_list():
    return [
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