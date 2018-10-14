# Here we create an Item Model which functions to serve as an internal representation of the object for the
# API. The resources are the external model. In general, resources should only have get,post,put,delete,etc.
from db import db
from datetime import datetime

# These models must extend db.Model, this creates the mapping between the db and the model objects
class DonationModel(db.Model):

    __tablename__ = "donations"
    id = db.Column(db.Integer, primary_key= True)

    title = db.Column(db.String(80))
    deviceName = db.Column(db.String(80))
    description = db.Column(db.String)
    timeStamp = db.Column(db.DateTime, default=datetime.utcnow)

    # Foreign key relationship to clinics
    hospitalID = db.Column(db.Integer, db.ForeignKey("hospitals.id"))
    hospital = db.relationship("HospitalModel")


    def __init__(self,title, deviceName, description, hospitalID):
        self.title = title
        self.deviceName = deviceName
        self.description = description
        self.hospitalID = hospitalID

    # Return a json representation of the model
    def json(self):
        return {"id":self.id,"title":self.title, "deviceName": self.deviceName, "description":self.description, "hospitalID": self.hospitalID, "timeStamp": str(self.timeStamp)}

    @classmethod
    def find_by_id(cls, id):
        # SQL Alchemy will automatically convert a row to an object. This is incredibly simple. This automatically returns an ItemModel object
        # The query will allow us to build a query really fast and autoconvert an object
        return cls.query.filter_by(id=id).first() # SELECT * FROM items WHERE name=? (name, ) We can even keep building up this filter if we want

    # Insert the particular instance of this class into the databaseself. This also performs updates, so we no longer need an update method
    def save_to_db(self):
        # Add one object. automatically converted from object to row
        db.session.add(self)
        db.session.commit()

    # Update the row in the db with this name with the information from this instance of the class
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
