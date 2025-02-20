import django_tables2 as tables
from django.utils.html import format_html
import datetime, time

d_fmt = '%Y-%m-%d'
t_fmt = '%H:%M:%S'

class ScheduleClassTable(tables.Table):
    date = tables.DateColumn(format='Y-m-d', short=True)
    timeStart = tables.Column(verbose_name="Time")
    scheduleType = tables.Column(verbose_name="scheduleType", visible=False)
    title = tables.Column()
    timeEnd = tables.Column(visible=False)
    bookingStatus = tables.BooleanColumn(verbose_name='Action')
    scheduleItemId = tables.Column(visible=False)

    def render_bookingStatus(self,value, record):
        if record['scheduleType'] == "class":
            if value:
                return format_html("<a class='btn' target='blank' href='https://book.ganeshyoga.de/#/shop/classes/book/{}/{}'> Book</a>", record['scheduleItemId'], record['date'])
            else:
                return ""
        else:
            if value:
                return format_html("<a class='btn' target='blank' href='https://book.ganeshyoga.de/#/shop/events/{}'>Book</a>", record['scheduleItemId'] )
            else: 
                return "No data {}".format(value)
    
    def render_timeStart(self, value, record):
        value = ':'.join(value.split(':')[:2])
        time_end = ':'.join(record['timeEnd'].split(':')[:2])
        return format_html('<b> {} - {}</b>', value, time_end)
    

    def render_date(self, value, record):
        new_value = value + ' ' + record['timeStart']
        dt_fmt = d_fmt + ' ' + t_fmt 
        return datetime.datetime.strptime(new_value, dt_fmt).date()
        
    
    class Meta:
        template_name = "django_tables2/semantic.html"
