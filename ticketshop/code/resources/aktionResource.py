# from flask_restful import Resource, reqparse
#
# from models.aktionModel import AktionModel
#
#
# class Aktion(Resource):
#     parser = reqparse.RequestParser()
#     parser.add_argument('rabatt', type =float, required = True, help="Es muss ein Rabatt eingegeben werden.")
#     parser.add_argument('strecken_id', type=int, required=False)
#
#
#     def get(self, _id):
#         aktion = AktionModel.find_by_id(_id)
#         if aktion:
#             return aktion.json()
#         return {"message": "Es existiert keine Aktion mit dieser Id."}, 400
#
#     def delete(self, _id):
#         aktion = AktionModel.find_by_id(_id)
#
#         if aktion:
#             aktion.delete_from_db()
#             return {"message": "Aktion erfolgreich geloescht."} # code = 200 ; muss nicht angegeben werden, weil default
#         return {"message": "Es existiert keine Aktion mit dieser Id."}, 400
#
#
# class AktionDelete(Resource):
#     def delete(self, _id):
#         aktion = AktionModel.find_by_id(_id)
#
#         if aktion:
#             aktion.delete_from_db()
#             return {"message": "Aktion erfolgreich geloescht."} # code = 200 ; muss nicht angegeben werden, weil default
#         return {"message": "Es existiert keine Aktion mit dieser Id."}, 400
#
#
# class Aktionen(Resource):
#     def get(self):
#         aktionen = AktionModel.find_all()
#         result = []
#         for aktion in aktionen:
#             result.append(aktion.json())
#         return result
#
#
# class Aktionsverwaltung(Resource):
#     parser = reqparse.RequestParser()
#     parser.add_argument('rabatt', type =float, required = True, help="Es muss ein Rabatt eingegeben werden.")
#     parser.add_argument('strecken_id', type=int, required=True)
#     parser.add_argument('abschnitt_id', type=int, required=True)
#     parser.add_argument('startdatum', type=str, required=True)
#     parser.add_argument('enddatum', type=str, required=True)
#
#     def post(self):
#         data = Aktionsverwaltung.parser.parse_args()
#         aktion = AktionModel(data['rabatt'], data['strecken_id'], data['abschnitt_id'], data['startdatum'], data['enddatum'])
#
#         if aktion.rabatt <= 0 or aktion.rabatt >= 100:
#             return {"message": "Der Rabatt muss größer als 0 und kleiner als 100 sein."}, 400
#         if aktion.strecken_id > 0 and aktion.abschnitt_id > 0:
#             return {"message": "Eine Aktion kann sich nicht auf eine Strecke und auf einen Abschnitt gleichzeitig beziehen."}, 400
#         if aktion.startdatum > aktion.enddatum:
#             return {"message": "Das Startdatum darf nicht nach dem Enddatum liegen."}, 400
#         # Check, ob Strecke bzw. Abschnitt existiert, ergänzen
#
#         try:
#             aktion.save_to_db()
#             return aktion.json(), 201
#         except:
#             return {"message": "Es ist leider ein Fehler bei der Aktionserstellung aufgetreten."}, 500
#
# class Aktionseditierung(Resource):
#     parser = reqparse.RequestParser()
#     parser.add_argument('rabatt', type=float, required=True, help="Es muss ein Rabatt eingegeben werden.")
#     parser.add_argument('strecken_id', type=int, required=True)
#     parser.add_argument('abschnitt_id', type=int, required=True)
#     parser.add_argument('startdatum', type=str, required=True)
#     parser.add_argument('enddatum', type=str, required=True)
#
#     def put(self, _id):
#         data = Aktion.parser.parse_args()
#         aktion = AktionModel.find_by_id(_id)
#         if aktion:
#             aktion.rabatt = data['rabatt']
#             aktion.strecken_id = data['strecken_id']
#             aktion.abschnitt_id = data['abschnitt_id']
#             aktion.startdatum = data['startdatum']
#             aktion.enddatum = data['enddatum']
#             if aktion.rabatt <= 0 or aktion.rabatt >= 100:
#                 return {"message": "Der Rabatt muss größer als 0 und kleiner als 100 sein."}, 400
#             if aktion.strecken_id > 0 and aktion.abschnitt_id > 0:
#                 return {"message": "Eine Aktion kann sich nicht auf eine Strecke und auf einen Abschnitt gleichzeitig beziehen."}, 400
#             if aktion.startdatum > aktion.enddatum:
#                 return {"message": "Das Startdatum darf nicht nach dem Enddatum liegen."}, 400
#             # Check, ob Strecke bzw. Abschnitt existiert, ergänzen
#
#             try:
#                 aktion.save_to_db()
#                 return aktion.json()
#             except:
#                 return {"message": "Es ist leider ein Fehler bei der Aktionserstellung aufgetreten."}, 500
#         return {"message": "Es existiert keine Strecke mit dieser Id."}, 400