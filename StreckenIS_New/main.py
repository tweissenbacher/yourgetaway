from flask_restful import Api

from website import create_app
from website.routes import Routes, Route
from website.sections import Sections, Section
from website.trainstations import Trainstations, Trainstation
from website.warnings import Warnings, Warning
from website.users import Users, User


app = create_app()
api = Api(app)

api.add_resource(Trainstation, "/trainstation/<int:trainstations_id>")
api.add_resource(Trainstations, "/all_trainstations")

api.add_resource(Section, "/section/<int:sections_id>")
api.add_resource(Sections, "/all_sections")

api.add_resource(Route, "/route/<int:route_id>")
api.add_resource(Routes, "/all_routes")

api.add_resource(Warning, "/warning/<int:warning_id>")
api.add_resource(Warnings, "/all_warnings")

api.add_resource(User, "/user/<int:user_id>")
api.add_resource(Users, "/all_users")

if __name__ == '__main__':
    app.run(debug=True)
