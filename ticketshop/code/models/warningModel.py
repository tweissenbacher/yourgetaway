class WarningModel:

    def __init__(self, id, text):
        self.id = id
        self.text = text

    @classmethod
    def json_to_object(cls, json_warning):
        id = json_warning['id']
        text = json_warning['warnings']
        return WarningModel(id, text)
