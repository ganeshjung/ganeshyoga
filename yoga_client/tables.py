import django_tables2 as tables
from django.utils.html import format_html
import datetime, time

d_fmt = '%Y-%m-%d'
t_fmt = '%H:%M:%S'

class ScheduleClassTable(tables.Table):
    date = tables.DateColumn(format='Y-m-d', short=True)
    timeStart = tables.Column(verbose_name="Time")
    frequencyType = tables.Column(verbose_name="FreqType", visible=False)
    account = tables.Column(verbose_name="Instructor", visible=False)
    organizationLocationRoom = tables.Column(verbose_name="Room", visible=False)
    organizationLocation = tables.Column(verbose_name="Location", visible=False)
    organizationClasstype = tables.Column(verbose_name="Title")
    organizationLevel = tables.Column(verbose_name="Level", visible=False)
    
    timeEnd = tables.Column(visible=False)
    spaces = tables.Column(visible=False)
    countAttending = tables.Column(visible=False)
    countBooked = tables.Column(visible=False)
    availableSpacesOnline = tables.Column(visible=False)
    availableSpacesTotal = tables.Column(visible=False)
    bookingStatus = tables.BooleanColumn(verbose_name='Action')
    scheduleItemId = tables.Column(visible=False)

    def render_bookingStatus(self,value, record):
        if value:
            return format_html("<a class='btn' target='blank' href='https://book.ganeshyoga.de/#/shop/classes/book/{}/{}'> Book</a>", record['scheduleItemId'], record['date'])
        else:
            return ""
    
    def render_timeStart(self, value, record):
        return format_html('<b> {} - {}</b>', value, record['timeEnd'])
    
    def render_spaces(self, value, record):
        return f"{record['availableSpacesTotal']} out of {value} available"
    

    def render_date(self, value, record):
        new_value = value + ' ' + record['timeStart']
        dt_fmt = d_fmt + ' ' + t_fmt 
        return datetime.datetime.strptime(new_value, dt_fmt).date()
        
    
    class Meta:
        template_name = "django_tables2/semantic.html"
