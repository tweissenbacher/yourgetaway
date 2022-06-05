from flask import flash

from db import db

class WarningModel:

    def __init__(self, id, text):
        self.id = id
        self.text = text

    @classmethod
    def json_to_object(cls, json_warning):
        id = json_warning['id']
        text = json_warning['text']
        return WarningModel(id, text)
