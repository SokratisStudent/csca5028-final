from app import db


class Country(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    country_code = db.Column("country_id", db.String(2))
    name = db.Column("country_name", db.String(50))
    has_data = db.Column("has_public_holiday_data", db.String(1))
