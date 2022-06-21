import allEndpoints

# serves the representation of trip objects which are fetched from the fahrplan-informationssystem
# not a DB-Model!
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

    # maps the json trip which is delivered by the fahrplan-informationssystem for the usage in the ticketshop
    @classmethod
    def json_to_object(cls, json_trip):
        note = json_trip['note']
        departure = json_trip['departure']
        train_id = int(json_trip['train_id'])
        train = allEndpoints.TrainEndpoint.find_by_id(train_id)['name']
        price = json_trip['price']
        date_start = json_trip['recurrence']['date_start']
        date_end = json_trip['recurrence']['date_end']
        weekdays = []
        if int(json_trip['recurrence']['mon']) == 1:
            weekdays.append('Monday')
        if int(json_trip['recurrence']['tue']) == 1:
            weekdays.append('Tuesday')
        if int(json_trip['recurrence']['wed']):
            weekdays.append('Wednesday')
        if int(json_trip['recurrence']['thu']) == 1:
            weekdays.append('Thursday')
        if int(json_trip['recurrence']['fri']) == 1:
            weekdays.append('Friday')
        if int(json_trip['recurrence']['sat']) == 1:
            weekdays.append('Saturday')
        if int(json_trip['recurrence']['sun']) == 1:
            weekdays.append('Sunday')
        # weekdays = json_trip['recurrence']['weekdays']

        return TripModel(note, departure, train_id, train, price, date_start, date_end, weekdays)

