from models.ClinicModel import ClinicModel
from flask_restful import Resource, reqparse

class ClinicResource(Resource):

    # Defining a parser that will handle data collection from post requests
    parser = reqparse.RequestParser()

    parser.add_argument("institution",
        type = str,
        required = True, # If there is no price argument, stop.
        help = "Instituion cannot be left blank"
    )

    def get(self,name):
        returnClinic = ClinicModel.find_by_name(name)
        if(returnClinic):
            return returnClinic.json()
        # If store is not found
        return {"message":"Clinic Not Found"}, 404

    def post(self,name):
        # Check if store already exists
        if(ClinicModel.find_by_name(name)):
            return {"message":"Clinic Already Exists"}, 400 # bad request
        # If store doesn't exist, create a new one
        newClinic = ClinicModel(name, 1)
        try:
            newClinic.save_to_db()
            return newClinic.json()
        except:
            return {"message":"Could not create new clinic"}, 500 # Internal server error

    def delete(self,name):
        clinicToDelete = ClinicModel.find_by_name(name)
        if(clinicToDelete):
            clinicToDelete.delete_from_db()
        # If the story didn't exist to begin with, we don't really care as long as it is no longer there
        return {"Message":"Clinic has been deleted"}

class ClinicListResource(Resource):

    def get(self):
        return [clinic.json() for clinic in ClinicModel.query.all()]
