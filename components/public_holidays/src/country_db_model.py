from components.database.main import db


class Country(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    country_code = db.Column("country_code", db.String(2))
    name = db.Column("country_name", db.String(50))
    latest_year_with_data = db.Column("latest_year_with_data", db.Integer)