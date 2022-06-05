from allEndpoints import SectionEndpoint

from models.warningModel import WarningModel


class SectionModel:

    def __init__(self, id, from_, to, time, costs, warnings):
        self.id = id
        self.from_ = from_
        self.to = to
        self.time = time
        self.costs = costs
        self.warnings = warnings

    @classmethod
    def json_to_object(cls, json_section):
        id_ = int(json_section['id'])
        from_ = json_section['start']
        to = json_section['end']
        time = json_section['time']
        costs = json_section['fee']
        warnings = []
        for warning in json_section['warnings']:
            warnings.append(WarningModel.json_to_object(warning))
        return SectionModel(id_, from_, to, time, costs, warnings)

    @classmethod
    def json_to_object_fahrplansystem(cls, json_section):
        return None


    @classmethod
    def find_section_from_to(cls, from_, to):
        sections = SectionEndpoint.find_all()
        sections = [cls.json_to_object(s) for s in sections]
        filtered_sections = list(filter(lambda x: (x.from_ == from_ and x.to == to) or (x.from_ == to and x.to == from_), sections))
        if len(filtered_sections) <= 0:
            return None
        return filtered_sections[0]

    @classmethod
    def get_section_dictionary(cls):
        all_sections = SectionEndpoint.find_all()
        all_sections = [cls.json_to_object(s) for s in all_sections]
        dictionary = {}
        for section in all_sections:
            dictionary[section.id] = section
        return dictionary


