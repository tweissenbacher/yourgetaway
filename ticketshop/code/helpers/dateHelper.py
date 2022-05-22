import datetime

from ticketshop.code.endpoints.dummyData.dummyDatenFahrtstrecken import DummyFahrtstrecken


class DateHelper:

    def get_weekday(date_str):
        date = DateHelper.transform_str_to_date(date_str)
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        dayNumber = date.weekday()
        return days[dayNumber]

    def get_time_for_ride(line_id, time_str, destination):
        line = DummyFahrtstrecken.getDummyFahrtstreckeById(line_id)
        sections = line['sections']
        date_format_str = '%Y-%m-%d %H:%M'
        time = datetime.datetime.strptime(time_str, date_format_str)

        for s in sections:
            if s['von'] == destination:
                return time.strftime('%Y-%m-%d %H:%M')
            time = time + datetime.timedelta(minutes=s['zeitdauer'])
        return time.strftime('%Y-%m-%d %H:%M')

    def transform_str_to_date(date_str):
        date_format_str = '%Y-%m-%d %H:%M'
        return datetime.datetime.strptime(date_str, date_format_str)