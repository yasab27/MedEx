# Here we create an Item Model which functions to serve as an internal representation of the object for the
# API. The resources are the external model. In general, resources should only have get,post,put,delete,etc.
from db import db

# These models must extend db.Model, this creates the mapping between the db and the model objects
class HospitalModel(db.Model):

    __tablename__ = "hospitals"
    id = db.Column(db.Integer, primary_key= True)
    name = db.Column(db.String(80))

    donations = db.relationship("DonationModel")

    def __init__(self,name):
        self.name = name

    # Return a json representation of the model
    def json(self):
        donationsJSON = [donation.json() for donation in self.donations]
        return {"id":self.id, "name":self.name, "donations": donationsJSON}

    @classmethod
    def find_by_name(cls, name):
        # SQL Alchemy will automatically convert a row to an object. This is incredibly simple. This automatically returns an ItemModel object
        # The query will allow us to build a query really fast and autoconvert an object
        return cls.query.filter_by(name=name).first() # SELECT * FROM items WHERE name=? (name, ) We can even keep building up this filter if we want

    # Insert the particular instance of this class into the databaseself. This also performs updates, so we no longer need an update method
    def save_to_db(self):
        # Add one object. automatically converted from object to row
        db.session.add(self)
        db.session.commit()

    # Update the row in the db with this name with the information from this instance of the class
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    # Return all the items in a json format
    @classmethod
    def returnAll(cls):
        allClinics =  cls.query.all()
        allClinicsJSON = [clinic.json() for clinic in allClinics]
        return allClinicsJSON
