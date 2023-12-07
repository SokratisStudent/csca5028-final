from components.database.main import db


class PersonalVacation(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'))
    start_date = db.Column("start_date", db.DateTime)
    end_date = db.Column("end_date", db.DateTime)



