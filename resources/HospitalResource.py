from models.HospitalModel import HospitalModel
from flask_restful import Resource, reqparse

class HospitalResource(Resource):

    def get(self,name):
        returnHospital = HospitalModel.find_by_name(name)
        if(returnHospital):
            return returnHospital.json()
        # If store is not found
        return {"message":"Hopsital Not Found"}, 404

    def post(self,name):
        # Check if store already exists
        if(HospitalModel.find_by_name(name)):
            return {"message":"Hospital Already Exists"}, 400 # bad request
        # If store doesn't exist, create a new one
        newHopsital = HospitalModel(name)
        try:
            newHopsital.save_to_db()
            return newHopsital.json()
        except:
            return {"message":"Could not create new hospital"}, 500 # Internal server error

    def delete(self,name):
        clinicToDelete = HospitalModel.find_by_name(name)
        if(clinicToDelete):
            clinicToDelete.delete_from_db()
        # If the story didn't exist to begin with, we don't really care as long as it is no longer there
        return {"Message":"Hospital has been deleted"}

class HospitalListResource(Resource):

    def get(self):
        return HospitalModel.returnAll()
