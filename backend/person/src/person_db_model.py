from backend.database.main import db


class Person(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column("name", db.String(100), unique=True, nullable=False)
    country_code = db.Column("country_code", db.String(2), db.ForeignKey('country.country_code'))
    country_name = db.Column("country_name", db.String(100))
    project_id = db.Column("project_id", db.Integer, db.ForeignKey('project.id'))
