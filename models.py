from app import db
from sqlalchemy import and_
from sqlalchemy.sql import text


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
    tek_systems_bucket = db.Column(db.String(255))
    overall_bucket = db.Column(db.String(255))
    grouping = db.Column(db.String(255))
    location = db.Column(db.String(255))


    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    
    date_modified = db.Column(
        db.DateTime, default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp())

    def __init__(self, primary_skill, location, bench, name, years, total_experience):
        self.primary_skill = primary_skill
        self.location = location
        self.bench = bench
        self.name = name
        self.years = years
        self.total_experience = total_experience

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all(primary_skill, location, bench):
        print("get_all")
        if bench is None:
            return Resourcelist.query.filter_by(primary_skill=primary_skill, location=location)
        else :
            return Resourcelist.query.filter_by(primary_skill=primary_skill , location=location , billable="No")

    @staticmethod
    def get_all_location(location):
        print("get_all_location")
        return Resourcelist.query.filter_by(location=location)

    @staticmethod
    def get_user(name):
        print("get_user")
        return Resourcelist.query.filter(Resourcelist.name.ilike('%'+name+'%')).first()

    @staticmethod
    def get_contact(username):
        print("get_contact")
        return Resourcelist.query.filter(Resourcelist.name.ilike('%'+username+'%')).first()

    @staticmethod
    def get_user_based_on_project(projectname):
        print("get_user_based_project")
        return Resourcelist.query.filter(Resourcelist.customer.ilike('%'+projectname+'%')).all()
        #db.engine.execute(text("SELECT * FROM resourcelists WHERE LOWER(customer) like LOWER('%'"+projectname+"'%')").execution_options(autocommit=True))

    @staticmethod
    def get_user_by_manager(reportingmanager):
        return Resourcelist.query.filter(Resourcelist.reporting_manager.ilike('%'+reportingmanager.lower()+'%')).all()

    @staticmethod
    def get_practices():
        return db.engine.execute(text("SELECT DISTINCT organization FROM resourcelists").execution_options(autocommit=True)).fetchall()
    
    @staticmethod
    def get_practice_headcount(practicename) :
        return str(len(Resourcelist.query.filter(Resourcelist.organization.ilike('%'+practicename.lower()+'%')).all()))

    @staticmethod
    def get_exp_lessthan(primary_skill, location, bench, years):
        print("get_exp_lessthan")
        if bench is None:
            return Resourcelist.query.filter(and_(Resourcelist.primary_skill==primary_skill, Resourcelist.location.ilike==location, Resourcelist.total_experience <= years)).all()
        else:
            return Resourcelist.query.filter(and_(Resourcelist.primary_skill==primary_skill, Resourcelist.location==location, Resourcelist.billable=="No", Resourcelist.tek_experience <= years)).all()

    @staticmethod
    def get_exp_greaterthan(primary_skill, location, bench, years):
        print("get_exp_greater_than")
        if bench is None:
            return Resourcelist.query.filter(and_(Resourcelist.primary_skill==primary_skill, Resourcelist.location==location, Resourcelist.total_experience > years)).all()
        else:
            return Resourcelist.query.filter(and_(Resourcelist.primary_skill==primary_skill, Resourcelist.location==location, Resourcelist.billable=="No", Resourcelist.tek_experience > years)).all()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return "<Resourcelist: {}>".format(self.name)
