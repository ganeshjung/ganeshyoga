import requests, datetime
from django.conf import settings
from typing import Tuple
d_fmt = "%Y-%m-%d"
url = getattr(settings, 'COSTASIELLA_DOMAIN') + '/d/graphql_app/'

def filter_active_class(data: dict) -> list[dict]:
    """ This function will filter data that can be booked. 
    Also deconstruct the dictionary for table structure
    Sample Input data: 
         {'date': '2025-02-10', 
         'bookingOpenOn': '2024-09-13', 
         'classes': [{'scheduleItemId': 
                      'U2NoZWR1bGVJdGVtTm9kZToyMA==', 
                      'frequencyType': 'WEEKLY', 
                      'date': '2025-02-10', 
                      'status': '', 
                      'holiday': False, 
                      'holidayName': '', 
                      'description': None, 
                      'account': {
                                  'id': 'QWNjb3VudE5vZGU6Mw==', 
                                  'fullName': 'Ganesh Puri', 
                                  '__typename': 'AccountNode'
                                 }, 
                      'role': '', 
                      'account2': None, 
                      'role2': '', 
                      'organizationLocationRoom': {
                            'id': 'T3JnYW5pemF0aW9uTG9jYXRpb25Sb29tTm9kZToz', 
                            'name': 'Yogaraum', 
                            'organizationLocation': {
                                'id': 'T3JnYW5pemF0aW9uTG9jYXRpb25Ob2RlOjI=', 
                                'name': 'Schieggashram', 
                                '__typename': 'OrganizationLocationNode'
                            }, 
                            '__typename': 'OrganizationLocationRoomNode'
                        }, 
                    'organizationClasstype': {
                        'id': 'T3JnYW5pemF0aW9uQ2xhc3N0eXBlTm9kZToy', 
                        'name': 'Hatha Yoga für Anfänger und Fortgeschrittene', 
                        '__typename': 'OrganizationClasstypeNode'
                        }, 
                    'organizationLevel': {
                       'id': 'T3JnYW5pemF0aW9uTGV2ZWxOb2RlOjI=', 
                       'name': 'Anfänger und Fortgeschrittene ', 
                       '__typename': 'OrganizationLevelNode'
                    }, 
                    'timeStart': '18:30:00', 
                    'timeEnd': '20:00:00', 
                    'spaces': 15, 
                    'countAttending': 0, 
                    'countBooked': 0, 
                    'countAttendingAndBooked': 0, 
                    'availableSpacesOnline': 15, 
                    'availableSpacesTotal': 15, 
                    'displayPublic': True, 
                    'bookingStatus': 'FINISHED', 
                    '__typename': 'ScheduleClassType'
                }], 
            '__typename': 'ScheduleClassesDayType'
        }

        Sample Output Data:
                  { 'date': '2025-02-10',
                   'frequencyType': 'WEEKLY',
                   'account': 'Ganesh Puri',
                   'organizationLocationRoom': 'Yogaraum',
                   'organizationLocation': 'Schieggashram', 
                   'organizationClasstype': 'Hatha Yoga für Anfänger und Fortgeschrittene', 
                   'organizationLevel': 'Anfänger und Fortgeschrittene ',
                   'timeStart': '18:30:00', 
                    'timeEnd': '20:00:00',
                    'spaces': 15, 
                    'countAttending': 0, 
                    'countBooked': 0, 
                    'availableSpacesOnline': 15, 
                    'availableSpacesTotal': 15, 
                    'bookingStatus': 'FINISHED',
                    'scheduleItemId': 'U2NoZWR1bGVJdGVtTm9kZToyMA==',
                    }

    """
    filtered_data = []
    for row in data['data']['scheduleClasses']:
        if row['classes']:
            # each day can contain multiple classes
            for class_data in row['classes']:
                row_data = {
                   'date': class_data['date'],
                   'frequencyType': class_data['frequencyType'],
                   'account': class_data['account']['fullName'],
                   'organizationLocationRoom': class_data['organizationLocationRoom']['name'],
                   'organizationLocation': class_data['organizationLocationRoom']['organizationLocation']['name'],
                   'organizationClasstype': class_data['organizationClasstype']['name'], 
                   'organizationLevel': class_data['organizationLevel']['name'],
                   'timeStart': class_data['timeStart'], 
                    'timeEnd': class_data['timeEnd'],
                    'spaces': class_data['spaces'], 
                    'countAttending': class_data['countAttending'], 
                    'countBooked': class_data['countBooked'], 
                    'availableSpacesOnline': class_data['availableSpacesOnline'], 
                    'availableSpacesTotal': class_data['availableSpacesTotal'], 
                    'bookingStatus': class_data['bookingStatus'],
                    'scheduleItemId': class_data['scheduleItemId'],
                    } 
                filtered_data.append(row_data)
        
    return filtered_data

def upcoming_classess(start_date: str, level: str = "", classtype: str = '')-> list[dict] :
    variables = {
        "dateFrom": start_date,
        "dateUntil": (datetime.datetime.strptime(start_date, d_fmt) + datetime.timedelta(days=6)).strftime(d_fmt),
        "organizationClasstype": classtype,
        "instructor": "",
        "organizationLevel": level,
        "organizationLocation": ""
    }

    data = {
    "operationName": "ScheduleClasses",
    "variables": variables,
    "query": "query ScheduleClasses($dateFrom: Date!, $dateUntil: Date!, $orderBy: String, $instructor: ID, $organizationClasstype: ID, $organizationLevel: ID, $organizationLocation: ID) {\n  scheduleClasses(\n    dateFrom: $dateFrom\n    dateUntil: $dateUntil\n    orderBy: $orderBy\n    instructor: $instructor\n    organizationClasstype: $organizationClasstype\n    organizationLevel: $organizationLevel\n    organizationLocation: $organizationLocation\n    publicOnly: false\n  ) {\n    date\n    bookingOpenOn\n    classes {\n      scheduleItemId\n      frequencyType\n      date\n      status\n      holiday\n      holidayName\n      description\n      account {\n        id\n        fullName\n        __typename\n      }\n      role\n      account2 {\n        id\n        fullName\n        __typename\n      }\n      role2\n      organizationLocationRoom {\n        id\n        name\n        organizationLocation {\n          id\n          name\n          __typename\n        }\n        __typename\n      }\n      organizationClasstype {\n        id\n        name\n        __typename\n      }\n      organizationLevel {\n        id\n        name\n        __typename\n      }\n      timeStart\n      timeEnd\n      spaces\n      countAttending\n      countBooked\n      countAttendingAndBooked\n      availableSpacesOnline\n      availableSpacesTotal\n      displayPublic\n      bookingStatus\n      __typename\n    }\n    __typename\n  }\n  instructors(first: 100) {\n    edges {\n      node {\n        id\n        fullName\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  organizationLocations(first: 100, archived: false) {\n    pageInfo {\n      startCursor\n      endCursor\n      hasNextPage\n      hasPreviousPage\n      __typename\n    }\n    edges {\n      node {\n        id\n        archived\n        name\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  organizationClasstypes(first: 100, archived: false) {\n    pageInfo {\n      startCursor\n      endCursor\n      hasNextPage\n      hasPreviousPage\n      __typename\n    }\n    edges {\n      node {\n        id\n        archived\n        name\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  organizationLevels(first: 100, archived: false) {\n    pageInfo {\n      startCursor\n      endCursor\n      hasNextPage\n      hasPreviousPage\n      __typename\n    }\n    edges {\n      node {\n        id\n        archived\n        name\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n"
    }
    
    with requests.session() as s:
        res = s.get(getattr(settings, 'COSTASIELLA_DOMAIN') + '/d/csrf')
        print(res.content)
        res = s.post(url, json=data, headers={"Accept": "application/json", "Content-Type": "application/json"})
        if res.status_code == 200:
            filtered_data = filter_active_class(res.json())
        else:
            print("We are not able to get any data. Reason: ", res.content)
            return []
        
        return filtered_data
    

def get_upcoming_classes(start_date, level="", classtype="", class_count=10):
    """ This function will bring number of upcoming classes by class_count
    """
    upcoming_class_data = []
    start_count = 0
    while start_count < class_count:
        # we need to keep looping until we atleast got 10 class for result
        filtered_data = upcoming_classess(start_date=start_date, level=level, classtype=classtype)
        if len(filtered_data) == 0:
            # No data received, we should assume no schedule is uploaded
            break
        else:
            start_count += len(filtered_data)
            upcoming_class_data += filtered_data
        
        start_date = (datetime.datetime.strptime(start_date, d_fmt) + datetime.timedelta(days=6)).strftime(d_fmt)
    
    return upcoming_class_data


def get_filter_set() -> dict:
    """ This page will get generate all the classtype and levels
    """

    data = {
    "query" : """query { 
                    organizationClasstypes(first: 100, archived: false) {
                        pageInfo {
                            startCursor
                            endCursor
                            hasNextPage
                            hasPreviousPage
                            __typename
                        }
                        edges {
                            node {
                            id
                            archived
                            name
                            __typename
                            }
                        __typename
                        }
                        __typename
                    }
                    organizationLevels(first: 100, archived: false) {
                        pageInfo {
                            startCursor
                            endCursor
                            hasNextPage
                            hasPreviousPage
                            __typename
                        }
                        edges {
                            node {
                                id
                                archived
                                name
                                __typename
                            }
                            __typename
                        }
                    } 
                }     
            """
        }
    
    with requests.session() as s:
        res = s.get(getattr(settings, 'COSTASIELLA_DOMAIN') + '/d/csrf')
        print(res.content)
        res = s.post(url, json=data, headers={"Accept": "application/json", "Content-Type": "application/json"})
        if res.status_code == 200:
            filter_set = res.json()
        else:
            print("We are not able to get any data. Reason: ", res.content)
            return {}
        
    return filter_set



    