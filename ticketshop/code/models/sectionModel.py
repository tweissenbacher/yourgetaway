from allEndpoints import SectionEndpoint
from models.warningModel import WarningModel

# serves the representation of section objects which are fetched from the strecken- and fahrplan-informationssystem
# not a DB-Model!
class SectionModel:

    def __init__(self, id, from_, to, time, costs, warnings):
        self.id = id
        self.from_ = from_
        self.to = to
        self.time = time
        self.costs = costs
        self.warnings = warnings

    # maps the json section which is delivered by the fahrplan-informationssystem for the usage in the ticketshop
    @classmethod
    def json_to_object(cls, json_section):
        id_ = int(json_section['id'])
        from_ = json_section['from_station_name']
        to = json_section['to_station_name']
        time = json_section['duration']
        costs = 0
        warnings = []
        return SectionModel(id_, from_, to, time, costs, warnings)

    # maps the json section which is delivered by the strecken-informationssystem for the usage in the ticketshop
    @classmethod
    def json_to_object_streckensystem(cls, json_section):
        id_ = int(json_section['id'])
        from_ = json_section['start']['name']
        to = json_section['end']['name']
        time = json_section['time']
        costs = json_section['fee']
        warnings = []
        for warning in json_section['section_warnings']:
            warnings.append(WarningModel.json_to_object(warning))
        return SectionModel(id_, from_, to, time, costs, warnings)

    # fetches a section given a certain start and end point
    @classmethod
    def find_section_from_to(cls, from_, to):
        sections = SectionEndpoint.find_all()
        sections = [cls.json_to_object_streckensystem(s) for s in sections]
        filtered_sections = list(filter(lambda x: (x.from_ == from_ and x.to == to) or (x.from_ == to and x.to == from_), sections))
        if len(filtered_sections) <= 0:
            return None
        return filtered_sections[0]

    # # returns a dictionary for all sections with the section id as key and the actual section as value
    # @classmethod
    # def get_section_dictionary(cls):
    #     all_sections = SectionEndpoint.find_all()
    #     all_sections = [cls.json_to_object_streckensystem(s) for s in all_sections]
    #     dictionary = {}
    #     for section in all_sections:
    #         dictionary[section.id] = section
    #     return dictionary


