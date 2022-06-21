# serves the representation of warning objects which are fetched from the strecken-informationssystem
# not a DB-Model!
class WarningModel:

    def __init__(self, id, text):
        self.id = id
        self.text = text

    # maps the json warning which is delivered by the strecken-informationssystem for the usage in the ticketshop
    @classmethod
    def json_to_object(cls, json_warning):
        id = json_warning['id']
        text = json_warning['warnings']
        return WarningModel(id, text)
