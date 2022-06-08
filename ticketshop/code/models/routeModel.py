from models.sectionModel import SectionModel

from allEndpoints import RouteEndpoint

class RouteModel:

    def __init__(self, id, from_, to, sections):
        self.id = id
        self.from_ = from_
        self.to = to
        self.sections = sections

    @classmethod
    def json_to_object(cls, json_route):
        id_ = int(json_route['id'])
        from_ = json_route['start']['name']
        to = json_route['end']['name']
        sections = []
        for section in json_route['route_sections']:
            sections.append(SectionModel.json_to_object_streckensystem(section))

        return RouteModel(id_, from_, to, sections)

    @classmethod
    def find_route_from_to(cls, from_, to):
        routes = RouteEndpoint.find_all()
        routes = [cls.json_to_object(r) for r in routes]
        filtered_routes = \
            list(filter(lambda x: (x.from_ == from_ and x.to == to) or (x.from_ == to and x.to == from_), routes))
        if len(filtered_routes ) <= 0:
            return None
        return filtered_routes[0]

    @classmethod
    def get_route_dictionary(cls):
        all_routes = RouteEndpoint.find_all()
        all_routes = [cls.json_to_object(r) for r in all_routes]
        dictionary = {}
        for route in all_routes:
            dictionary[route.id] = route

        return dictionary
