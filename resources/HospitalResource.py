from models.HospitalModel import HospitalModel
from flask_restful import Resource, reqparse

class HospitalResource(Resource):

    parser = reqparse.RequestParser()

    parser.add_argument("email",
        type = str,
        required = True, # If there is no price argument, stop.
        help = "Title cannot be left blank"
    )

    parser.add_argument("password",
        type = str,
        required = True, # If there is no price argument, stop.
        help = "deviceName cannot be left blank"
    )

    def get(self,name):
        returnHospital = HospitalModel.find_by_name(name)
        if(returnHospital):
            return returnHospital.json()
        # If store is not found
        return {"message":"Hopsital Not Found"}, 404

    def post(self,name):

        data = HospitalResource.parser.parse_args()

        # Check if store already exists
        if(HospitalModel.find_by_name(name)):
            return {"message":"Hospital Already Exists"}, 400 # bad request
        # If store doesn't exist, create a new one
        newHopsital = HospitalModel(name,data["email"],data["password"])
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

class HospitalAuthenticationResource(Resource):

    parser = reqparse.RequestParser()

    parser.add_argument("email",
        type = str,
        required = True, # If there is no price argument, stop.
        help = "email cannot be left blank"
    )

    parser.add_argument("password",
        type = str,
        required = True, # If there is no price argument, stop.
        help = "password cannot be left blank"
    )

    def post(self):
        data = HospitalAuthenticationResource.parser.parse_args();

        email = data["email"]
        password = data["password"]

        hospital = HospitalModel.find_by_email(email)
        if hospital is None:
            return {"error":"No hospital with this email found"}
        if(hospital.password == password):
            return hospital.json()

        return {"Authentication failed for hospital"}
