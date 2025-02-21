import requests, datetime
from django.conf import settings
from typing import Tuple
d_fmt = "%Y-%m-%d"
dt_fmt = "%Y-%m-%d %H:%M:%S"
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
                    'scheduleType': 'class', # default value
                   'organizationClasstype': 'Hatha Yoga für Anfänger und Fortgeschrittene', 
                   'timeStart': '18:30:00', 
                    'timeEnd': '20:00:00',
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
                   'scheduleType': "class",
                   'title': class_data['organizationClasstype']['name'], 
                   'timeStart': class_data['timeStart'], 
                    'timeEnd': class_data['timeEnd'],
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
        res = s.post(url, json=data)
        if res.status_code == 200:
            filtered_data = filter_active_class(res.json())
        else:
            print("We are not able to get any data. Reason:", res.content)
            return []
        
        return filtered_data
    

def sort_filtered_data(data_list: list) -> list:
    """ this will filter out data based on start datetime 
    
    """
    sorted_list = []
    mydict = {}
    for data in data_list:
        # create key
        data_key = datetime.datetime.strptime(data['date'] + " " + data['timeStart'], dt_fmt)
        mydict[data_key.timestamp()] = data
    
    # get the sort by keyname
    for d in sorted(mydict.items()):
        sorted_list.append(d[1])


    return sorted_list
    


def get_upcoming_all(start_date, class_count=10):
    """ This function will bring number of upcoming classes by class_count
    """
    filtered_event = []
    upcoming_class_data = []
    start_count = 0
    while start_count < class_count:
        # we need to keep looping until we atleast got 10 class for result
        filtered_data = upcoming_classess(start_date=start_date, level="", classtype="")
        end_date = (datetime.datetime.strptime(start_date, d_fmt) + datetime.timedelta(days=7)).strftime(d_fmt)
        filtered_event = get_schedule_events(start_date=start_date, end_date=end_date)
        if len(filtered_data) == 0:
            # No data received, we should assume no schedule is uploaded
            break
        else:
            start_count += ( len(filtered_data ) + len(filtered_event))
            upcoming_class_data += sort_filtered_data(filtered_data + filtered_event)
        
        # change, next_start date to 7. Not 6
        start_date = (datetime.datetime.strptime(start_date, d_fmt) + datetime.timedelta(days=7)).strftime(d_fmt)
    

    
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


def filter_all_future_events(data: dict, start_date: str, end_date: str, level:str="") -> list[dict]:
    """ This will filter all future upcoming events taking start_date
    
    Sample data:
    {
  "scheduleEvents": {
    "pageInfo": {
      "hasNextPage": false,
      "hasPreviousPage": false,
      "startCursor": "YXJyYXljb25uZWN0aW9uOjA=",
      "endCursor": "YXJyYXljb25uZWN0aW9uOjU=",
      "__typename": "PageInfo"
    },
    "edges": [
      {
        "node": {
          "id": "U2NoZWR1bGVFdmVudE5vZGU6MQ==",
          "archived": false,
          "displayPublic": true,
          "displayShop": true,
          "autoSendInfoMail": false,
          "organizationLocation": {
            "id": "T3JnYW5pemF0aW9uTG9jYXRpb25Ob2RlOjI=",
            "name": "Schieggashram",
            "__typename": "OrganizationLocationNode"
          },
          "name": "Lakshmi Puja zur Wintersonnwende",
          "tagline": "Am dunkelsten Tag des Jahres feiern wir eine Puja zu Ehren von Lakshmi, der Göttin des Lichts.",
          "preview": "<p>Pujaabend mit Asanas, Meditation, Verehrung der G&ouml;ttin, Abendessen, Musik und je nach Wetter und Stimmung Tanz oder Feuer im Garten.</p>",
          "description": "<ul class=\"n8H08c UVNKR \">\n<li class=\"zfr3Q TYR86d eD0Rn \" dir=\"ltr\">\n<p class=\"zfr3Q CDt4Ke \" dir=\"ltr\" role=\"presentation\"><span class=\"C9DxTc \">16:00 Yogastunde</span></p>\n</li>\n<li class=\"zfr3Q TYR86d eD0Rn \" dir=\"ltr\">\n<p class=\"zfr3Q CDt4Ke \" dir=\"ltr\" role=\"presentation\"><span class=\"C9DxTc \">18:00 Puja mit Asanas, Meditation, Verehrung der G&ouml;ttin, Abendessen und Musik</span></p>\n</li>\n<li class=\"zfr3Q TYR86d eD0Rn \" dir=\"ltr\">\n<p class=\"zfr3Q CDt4Ke \" dir=\"ltr\" role=\"presentation\"><span class=\"C9DxTc \">20:00 Yoga Ecstatic Dance und/oder Feuer im Garten</span></p>\n</li>\n</ul>",
          "organizationLevel": {
            "id": "T3JnYW5pemF0aW9uTGV2ZWxOb2RlOjI=",
            "name": "Anfänger und Fortgeschrittene ",
            "__typename": "OrganizationLevelNode"
          },
          "instructor": {
            "id": "QWNjb3VudE5vZGU6Mw==",
            "fullName": "Ganesh   ",
            "__typename": "AccountNode"
          },
          "instructor2": null,
          "dateStart": "2024-12-21",
          "dateEnd": "2024-12-21",
          "timeStart": "16:00:00",
          "timeEnd": "21:00:00",
          "infoMailContent": "",
          "scheduleItems": {
            "edges": [
              {
                "node": {
                  "id": "U2NoZWR1bGVJdGVtTm9kZTo2",
                  "__typename": "ScheduleItemNode"
                },
                "__typename": "ScheduleItemNodeEdge"
              },
              {
                "node": {
                  "id": "U2NoZWR1bGVJdGVtTm9kZTo3",
                  "__typename": "ScheduleItemNode"
                },
                "__typename": "ScheduleItemNodeEdge"
              },
              {
                "node": {
                  "id": "U2NoZWR1bGVJdGVtTm9kZTo4",
                  "__typename": "ScheduleItemNode"
                },
                "__typename": "ScheduleItemNodeEdge"
              }
            ],
            "__typename": "ScheduleItemNodeConnection"
          },
          "media": {
            "pageInfo": {
              "hasNextPage": false,
              "hasPreviousPage": false,
              "startCursor": "YXJyYXljb25uZWN0aW9uOjA=",
              "endCursor": "YXJyYXljb25uZWN0aW9uOjA=",
              "__typename": "PageInfo"
            },
            "edges": [
              {
                "node": {
                  "urlImageThumbnailSmall": "/d/media/cache/0c/66/0c66889766c8f9f3920eda7435fe402d.jpg",
                  "urlImageThumbnailLarge": "/d/media/cache/97/41/9741dcb31667f169b5268e3b42e0d5ea.jpg",
                  "__typename": "ScheduleEventMediaNode"
                },
                "__typename": "ScheduleEventMediaNodeEdge"
              }
            ],
            "__typename": "ScheduleEventMediaNodeConnection"
          },
          "createdAt": "2024-12-08T12:53:53.310257+00:00",
          "updatedAt": "2024-12-08T12:57:31.112342+00:00",
          "__typename": "ScheduleEventNode"
        },
        "__typename": "ScheduleEventNodeEdge",
        "booking_link": "https://book.ganeshyoga.de/#/shop/events/U2NoZWR1bGVFdmVudE5vZGU6MQ==/ticket/U2NoZWR1bGVFdmVudFRpY2tldE5vZGU6MQ==",
      },

    ],
    "__typename": "ScheduleEventNodeConnection"
     }
    }
    
    Need to check that rows comes between start date and end date
    if level is given, it will filter out all rows matching the level
    """
    today = datetime.datetime.strptime(start_date, d_fmt)
    until = datetime.datetime.strptime(end_date, d_fmt)

    upcoming_events = []

    # Loop the result until we get date greater than or equal to today
    for node in data['scheduleEvents']['edges']:
        event = node['node']
        event_start_date = datetime.datetime.strptime(event['dateStart']+ ' '+ event['timeStart'], '%Y-%m-%d %H:%M:%S')
        event_end_date  = datetime.datetime.strptime(event['dateEnd']+ ' '+ event['timeEnd'], '%Y-%m-%d %H:%M:%S')
        if event_start_date > today and event_end_date < until and not level:
            row_data = {
                    'date': event['dateStart'],
                    'scheduleType': "event",
                   'title': event['name'], 
                   'timeStart': event['timeStart'], 
                    'timeEnd': event['timeEnd'],
                    'bookingStatus': "True",
                    'scheduleItemId': event['id'],
            }
            upcoming_events.append(row_data)
        elif event_start_date > today and event_end_date < until and level:
            if event['organizationLevel']['id'] == level:
                row_data = {
                        'date': event['dateStart'],
                        'scheduleType': "event",
                       'title': event['name'], 
                       'timeStart': event['timeStart'], 
                        'timeEnd': event['timeEnd'],
                         'bookingStatus': "True",
                        'scheduleItemId': event['id'],
                    }
            
                upcoming_events.append(row_data)
            else:
                continue

    return upcoming_events




def get_schedule_events(start_date: str, end_date:str, level:str="") -> list[dict]:
    data = {
    "operationName": "ScheduleEvents",
    "variables": {},
    "query": "query ScheduleEvents($before: String, $after: String) {\n  scheduleEvents(\n    first: 100\n    before: $before\n    after: $after\n    archived: false\n    displayShop: true\n  ) {\n    pageInfo {\n      hasNextPage\n      hasPreviousPage\n      startCursor\n      endCursor\n      __typename\n    }\n    edges {\n      node {\n        id\n        archived\n        displayPublic\n        displayShop\n        autoSendInfoMail\n        organizationLocation {\n          id\n          name\n          __typename\n        }\n        name\n        tagline\n        preview\n        description\n        organizationLevel {\n          id\n          name\n          __typename\n        }\n        instructor {\n          id\n          fullName\n          __typename\n        }\n        instructor2 {\n          id\n          fullName\n          __typename\n        }\n        dateStart\n        dateEnd\n        timeStart\n        timeEnd\n        infoMailContent\n        scheduleItems {\n          edges {\n            node {\n              id\n              __typename\n            }\n            __typename\n          }\n          __typename\n        }\n        media(first: 1) {\n          pageInfo {\n            hasNextPage\n            hasPreviousPage\n            startCursor\n            endCursor\n            __typename\n          }\n          edges {\n            node {\n              urlImageThumbnailSmall\n              urlImageThumbnailLarge\n              __typename\n            }\n            __typename\n          }\n          __typename\n        }\n        createdAt\n        updatedAt\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n"
    }

    with requests.session() as s:
        res = s.get(getattr(settings, 'COSTASIELLA_DOMAIN') + '/d/csrf')
        print(res.content)
        res = s.post(url, json=data)
        if res.status_code == 200: 

            all_events = filter_all_future_events(data=res.json()['data'], start_date =start_date, end_date=end_date, level=level)
        else:
            print("We are not able to get any data. Reason: ", res.content)
            return []
    
    return all_events


def get_upcoming_classes(start_date, level:str ="", classtype:str ="", class_count=10):
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
            start_count += len(filtered_data ) 
            upcoming_class_data +=  filtered_data 
        
        # change, next_start date to 7. Not 6
        start_date = (datetime.datetime.strptime(start_date, d_fmt) + datetime.timedelta(days=7)).strftime(d_fmt)

    
    return upcoming_class_data


def get_upcoming_events(start_date, level:str = "", class_count=10):
    """ This function will bring number of events by class_count
    """
    filtered_event = []
    end_date = (datetime.datetime.strptime(start_date, d_fmt) + datetime.timedelta(days=180)).strftime(d_fmt)
    filtered_event = get_schedule_events(start_date=start_date, end_date=end_date, level=level)
    if len(filtered_event) > class_count:
        return filtered_event[:class_count]
  
    return filtered_event