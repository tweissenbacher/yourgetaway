import datetime
from flask import flash
from db import db
from models.userModel import UserModel
from models.sectionModel import SectionModel
from allEndpoints import TrainEndpoint, LineEndpoint
from models.tripModel import TripModel

# serves the representation of line objects which are fetched from the fahrplan-informationssystem
# not a DB-Model!
class LineModel:

    def __init__(self, id, route_id, starting_point, destination, sections, trips):
        self.id = id
        self.route_id = route_id
        self.starting_point = starting_point
        self.destination = destination
        self.sections = sections
        self.trips = trips

    # maps the json line which is delivered by the fahrplan-informationssystem for the usage in the ticketshop
    @classmethod
    def json_to_object(cls, json_line):
        id = int(json_line['id'])
        route_id = int(json_line['route_id'])
        sections = []
        for section in json_line['sections']:
            # sections.append(SectionModel.json_to_object(section)) # section['section']
            sections.append(SectionModel.json_to_object(section['section']))
        if len(sections) > 0:
            starting_point = sections[0]
            destination = sections[-1]
        else:
            starting_point = None
            destination = None
        trips = []
        for trip in json_line['trips']:
            trips.append(TripModel.json_to_object(trip))

        return LineModel(id, route_id, starting_point, destination, sections, trips)

    # returns only those sections of a given line which are relevant (given a certain start and end point)
    @classmethod
    def get_relevant_sections(cls, line_id, from_, to):
        sections = LineModel.json_to_object(LineEndpoint.find_by_id(int(line_id))).sections
        relevant_sections = []
        from_found = False
        for section in sections:
            if section.from_ == to:
                break
            if section.from_ == from_:
                from_found = True
            if from_found:
                relevant_sections.append(section)
        return relevant_sections

    # returns all  existing line stations
    @classmethod
    def get_all_stations(cls):
        lines = [LineModel.json_to_object(line) for line in LineEndpoint.find_all()]
        stations = []
        for line in lines:
            for section in line.sections:
                if section.from_ not in stations:
                    stations.append(section.from_)
                if section.to not in stations:
                    stations.append(section.to)
        stations.sort()
        return stations
