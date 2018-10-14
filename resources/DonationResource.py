from models.DonationModel import DonationModel
from models.HospitalModel import HospitalModel
from flask_restful import Resource, reqparse

class DonationResource(Resource):
    # Defining a parser that will handle data collection from post requests
    parser = reqparse.RequestParser()

    parser.add_argument("title",
        type = str,
        required = True, # If there is no price argument, stop.
        help = "Title cannot be left blank"
    )

    parser.add_argument("deviceName",
        type = str,
        required = True, # If there is no price argument, stop.
        help = "deviceName cannot be left blank"
    )

    parser.add_argument("description",
        type = str,
        required = True, # If there is no price argument, stop.
        help = "description cannot be left blank"
    )

    parser.add_argument("hospitalID",
        type = str,
        required = True, # If there is no price argument, stop.
        help = "hospitalID cannot be left blank"
    )

    def get(self,id):
        returnRequest = RequestModel.find_by_id(id)
        if(returnRequest):
            return returnRequest.json()
        # If store is not found
        return {"message":"Request Not Found"}, 404

    def post(self):
        # Check if store already exists
        data = DonationResource.parser.parse_args();

        # If store doesn't exist, create a new one
        newDonation = DonationModel(**data)
        try:
            newDonation.save_to_db()
            return newDonation.json()
        except:
            return {"message":"Could not create new donation"}, 500 # Internal server error

    def delete(self,id):
        donationToDelete = DonationModel.find_by_id(id)
        if(donationToDelete):
            donationToDelete.delete_from_db()
        # If the story didn't exist to begin with, we don't really care as long as it is no longer there
        return {"Message":"Donation has been deleted"}

class DonationListResource(Resource):

    def get(self):
        return DonationModel.returnAll()
