import datetime
from flask import flash

from db import db

from models.userModel import UserModel
from models.sectionModel import SectionModel
from allEndpoints import TrainEndpoint, LineEndpoint
from models.tripModel import TripModel


class LineModel:

    def __init__(self, id, route_id, starting_point, destination, sections, trips):
        self.id = id
        self.route_id = route_id
        self.starting_point = starting_point
        self.destination = destination
        self.sections = sections
        self.trips = trips

    @classmethod
    def json_to_object(cls, json_line):
        id = int(json_line['id'])
        route_id = int(json_line['route_id'])
        sections = []
        for section in json_line['sections']:
            sections.append(SectionModel.json_to_object(section)) # section['section']
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
