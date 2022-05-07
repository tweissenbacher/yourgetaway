from flask_restful import Api

from website import create_app
from website.routes import Routes, Route
from website.sections import Sections, Section
from website.trainstations import Trainstations, Trainstation

app = create_app()
api = Api(app)

api.add_resource(Trainstation, "/trainstation/<int:trainstations_id>")
api.add_resource(Trainstations, "/all_trainstations")

api.add_resource(Section, "/section/<int:sections_id>")
api.add_resource(Sections, "/all_sections")

api.add_resource(Route, "/route/<int:route_id>")
api.add_resource(Routes, "/all_routes")

if __name__ == '__main__':
    app.run(debug=True)
