from django.shortcuts import render
from .tables import ScheduleClassTable
from .utils import get_upcoming_classes, get_upcoming_all, get_upcoming_events, get_filter_set, d_fmt
import datetime
from django.core.cache import cache
from django.views.decorators.clickjacking import xframe_options_exempt
# Create your views here.

@xframe_options_exempt
def classes_list(request):
    current_date = datetime.datetime.today().strftime(d_fmt)
    filter_type = request.GET.get('filter', '')
    if filter_type == 'class':
        # Need to get class data
        event_level = request.GET.get('event_level','')
        class_type = request.GET.get('class_type', '')
        key_name = '_'.join(['classes', current_date, class_type or 'no_cls', event_level or 'no_lvl'])
        if not cache.get(key_name):
            print('key:' , key_name, 'for class not found. creating')
            data = get_upcoming_classes(start_date=current_date, level=event_level, classtype=class_type)
            cache.set(key_name, data, timeout=300)
        else:
            data = cache.get(key_name)
    
    elif filter_type == 'event':
        # Need to get event data
        event_level = request.GET.get('event_level','')
        key_name = '_'.join(['events', current_date,  event_level or 'no_lvl'])
        if not cache.get(key_name):
            print('key :' , key_name, 'for events not found. creating')
            data = get_upcoming_events(start_date=current_date, level=event_level)
            cache.set(key_name, data, timeout=300)
        else:
            data = cache.get(key_name)

    else:
        # We have to fetch all latest.
        key_name = '_'.join(['latest', current_date, 'no_cls', 'no_lvl'])
        if not cache.get(key_name):
            print('key :' , key_name, 'for all not found. creating')
            data = get_upcoming_all(start_date=current_date)
            cache.set(key_name, data, timeout=300)
        else:
            data = cache.get(key_name)
    
    # finally we have data to show
    table = ScheduleClassTable(data)

    return render(request, 'yoga_client/classes_list.html', {"table": table})


def display_filter(request):
    """ This page will display all filter set available from Classtype and class level
    """
    if cache.get('filter_set'):
        data = cache.get('filter_set')
    else:
        data = get_filter_set()
        cache.set('filter_set', data, timeout=300)
    
    return render(request, 'yoga_client/filters.html', context={'data': data['data']})

