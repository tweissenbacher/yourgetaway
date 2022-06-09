import datetime
from allEndpoints import LineEndpoint
from models.lineModel import LineModel


class DateHelper:

    def get_weekday(date_str):
        date = DateHelper.transform_str_to_date(date_str)
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        dayNumber = date.weekday()
        return days[dayNumber]

    def get_time_for_ride(line_id, time_str, destination):
        line = LineModel.json_to_object(LineEndpoint.find_by_id(line_id))
        sections = line.sections
        date_format_str = '%Y-%m-%d %H:%M'
        time = datetime.datetime.strptime(time_str, date_format_str)

        for s in sections:
            if s.from_ == destination:
                return time.strftime('%Y-%m-%d %H:%M')
            time = time + datetime.timedelta(minutes=s.time)
        return time.strftime('%Y-%m-%d %H:%M')

    def transform_str_to_date(date_str):
        date_format_str = '%Y-%m-%d %H:%M'
        return datetime.datetime.strptime(date_str, date_format_str)

    @classmethod
    def get_today(cls):
        today = (str(datetime.datetime.now())).rsplit(":", 1)[0]
        return today

    @classmethod
    def get_next_day(cls, date_str):
        date = DateHelper.transform_str_to_date(date_str)
        date = date + datetime.timedelta(minutes=1440) # next day
        new_date_str = date.strftime('%Y-%m-%d %H:%M')
        new_date_str = new_date_str.split(' ')[0] + " 00:01"
        return new_date_str

