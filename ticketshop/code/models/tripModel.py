class TripModel:

    def __init__(self, note, departure, train_id, train, price, date_start, date_end, weekdays):
        self.note = note
        self.departure = departure
        self.train_id = train_id
        self. train = train
        self.price = price
        self.date_start = date_start
        self.date_end = date_end
        self.weekdays = weekdays

    @classmethod
    def json_to_object(cls, json_trip):
        note = json_trip['note']
        departure = json_trip['departure']
        train_id = int(json_trip['train_id'])
        train = json_trip['train']
        price = json_trip['price']
        date_start = json_trip['recurrence']['date_start']
        date_end = json_trip['recurrence']['date_end']
        weekdays = []
        if bool(json_trip['recurrence']['mon']):
            weekdays.append('Monday')
        if bool(json_trip['recurrence']['tue']):
            weekdays.append('Tuesday')
        if bool(json_trip['recurrence']['wed']):
            weekdays.append('Wednesday')
        if bool(json_trip['recurrence']['thu']):
            weekdays.append('Thursday')
        if bool(json_trip['recurrence']['fri']):
            weekdays.append('Friday')
        if bool(json_trip['recurrence']['sat']):
            weekdays.append('Saturday')
        if bool(json_trip['recurrence']['sun']):
            weekdays.append('Sunday')
        # weekdays = json_trip['recurrence']['weekdays']

        return TripModel(note, departure, train_id, train, price, date_start, date_end, weekdays)

