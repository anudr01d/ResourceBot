# app/models.py

from app import db

class Resourcelist(db.Model):

    __tablename__ = 'resourcelists'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    empnumber = db.Column(db.String(255))
    designation = db.Column(db.String(255))
    employeetype= db.Column(db.String(255))
    email= db.Column(db.String(255))
    psft_id = db.Column(db.Integer)
    date_of_joining = db.Column(db.DateTime)
    tek_experience = db.Column(db.Float)
    past_experience = db.Column(db.Float)
    total_experience= db.Column(db.Float)
    family = db.Column(db.String(255))
    manager = db.Column(db.String(255))
    reporting_manager = db.Column(db.String(255))
    level_1_manager = db.Column(db.String(255))
    project = db.Column(db.String(255))
    billable = db.Column(db.String(255))
    organization = db.Column(db.String(255))
    primary_skill = db.Column(db.String(255))
    customer = db.Column(db.String(255))
    sales_manager = db.Column(db.String(255))
    delivery_manager = db.Column(db.String(255))
    pmo_owner = db.Column(db.String(255))
    tek_systems_bucket = db.Column(db.String(255))
    overall_bucket = db.Column(db.String(255))
    offshore_dm = db.Column(db.String(255))


    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    
    date_modified = db.Column(
        db.DateTime, default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp())

    def __init__(self, primary_skill):
        self.primary_skill = primary_skill

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all(primary_skill):
        print("Prmary skill : ", primary_skill)
        return Resourcelist.query.filter_by(primary_skill=primary_skill)

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return "<Resourcelist: {}>".format(self.name)
