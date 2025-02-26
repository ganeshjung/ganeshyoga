import django_tables2 as tables
from django.utils.html import format_html
import datetime, time

d_fmt = '%Y-%m-%d'
t_fmt = '%H:%M'

class ScheduleClassTable(tables.Table):
    date = tables.Column(visible=False)
    timeStart = tables.Column(verbose_name="From", 
                              attrs={"th": {"style": "text-align: right"},
                                     "td": {"style":"text-align: right" },
                                     }
                            )
    dashCol = tables.Column(default="-", verbose_name="",
                            attrs={"td": {"style": "text-align: center"}})
    
    timeEnd = tables.Column(verbose_name="To",
                            attrs={"th": {"style": "text-align: left"},
                                   "td": {"style":"text-align: left" },
                                  }
                            )
    scheduleType = tables.Column(verbose_name="scheduleType", visible=False)
    title = tables.Column()
    bookingStatus = tables.BooleanColumn(verbose_name="Action")
    scheduleItemId = tables.Column(visible=False)

    def render_dashCol(self, value):
        return format_html('<b>{}</b>'.format(value))
    

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
        startdate = datetime.datetime.strptime(record['date'], d_fmt)
        value = ':'.join(value.split(':')[:2])
        if datetime.datetime.now().year == startdate.year:
            startfrom = startdate.strftime('%a ') + startdate.strftime('%d.%m.').lstrip('0').replace('.0', '.')
        else:
            startfrom = startdate.strftime('%a ') + startdate.strftime('%d.%m.%y').lstrip('0').replace('.0', '.')
        
        return format_html('<b>{} {}</b>', startfrom, value)
    
    
    def render_timeEnd(self, value, record):
        endtime = ':'.join(value.split(':')[:2])
        if record['scheduleType'] == 'event':
            # Need to just render end time, but first check if the startDate equls EndDate
            if record['date'] != record['dateEnd']:
                # render date time short format 
                enddate = datetime.datetime.strptime(record['dateEnd'], d_fmt)
                if datetime.datetime.now().year == enddate.year:
                    endfrom = enddate.strftime('%a ') + enddate.strftime('%d.%m.').lstrip('0').replace('.0', '.')
                else:
                    endfrom = enddate.strftime('%a ') + enddate.strftime('%d.%m.%y').lstrip('0').replace('.0', '.')
                return format_html('<b>{} {}</b>'.format(endfrom, endtime))
        
        # render default time only
        return format_html('<b> {} </b> '.format(endtime))
    

    def render_date(self, value, record):
        new_value = value + ' ' + record['timeStart']
        dt_fmt = d_fmt + ' ' + t_fmt 
        return datetime.datetime.strptime(new_value, dt_fmt).date()
        
    
    class Meta:
        template_name = "django_tables2/semantic.html"
