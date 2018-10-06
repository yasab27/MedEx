# This defines the Strain Resource that will be used for CRUD operations in the API

# Importing necessary dependencies
from flask import Flask, request
from flask_restful import Resource, reqparse
from models.ProfessorModel import ProfessorModel
from db import db

class ProfessorResource(Resource):

    # GET a particular strain's information by id
    def get(self,uniqueID):
        professorOfInterest = ProfessorModel.find_by_id(uniqueID)
        if(professorOfInterest):
            return professorOfInterest.json()

        return {"message":"No professor could be found with that ID"}

# A resource to return a list of all strains in the db
class ProfessorListResource(Resource):

    # Return all strains in a json format
    def get(self):
        return ProfessorModel.return_all_professors()

# A resource to register a new strain
class ProfessorRegistrar(Resource):

    # Defining a parser that will handle data collection from post requests
    parser = reqparse.RequestParser()

    parser.add_argument("uniqueID",
        type = str,
        required = True, # If there is no price argument, stop.
        help = "UniqueID cannot be left blank"
    )

    parser.add_argument("firstName",
        type = str,
        required = True, # If there is no price argument, stop.
        help = "First name cannot be left blank"
    )

    parser.add_argument("lastName",
        type = str,
        required = True, # If there is no price argument, stop.
        help = "Last Name cannot be left blank"
    )

    parser.add_argument("genderPronouns",
        type = int,
        required = True, # If there is no price argument, stop.
        help = "Gender pronouncs cannot be left blank"
    )

    parser.add_argument("department",
        type = int,
        required = True, # If there is no price argument, stop.
        help = "Department cannot be left blank"
    )

    parser.add_argument("title",
        type = str,
        required = True, # If there is no price argument, stop.
        help = "Title cannot be left blank"
    )

    parser.add_argument("school",
        type = int,
        required = True, # If there is no price argument, stop.
        help = "School cannot be left blank"
    )

    # Create a new strain, add it to the table
    def post(self):

        # Acquire all of the data in a dict of each argument defined in the parser above.
        data = ProfessorRegistrar.parser.parse_args();

        # Error trapping to see if a professor already exists with that particular idea
        if(ProfessorModel.find_by_id(data.uniqueID)):
            return {"Error":"A professor with that Unique ID already exists"}

        # Create a new ProfessorModel object containing the passed properties.
        newProf = ProfessorModel(**data) ## ** automatically separates dict keywords into arguments

        # Save the new professor to the database.
        newProf.save_to_db()

        return ProfessorModel.return_last_item().json()