from main import db


class Person(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    country_code = db.Column("country_id", db.String(2))
    name = db.Column("name", db.String(50))
