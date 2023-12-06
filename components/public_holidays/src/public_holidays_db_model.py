from main import db


class PublicHoliday(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    country_code = db.Column("country_id", db.String(2))
    name = db.Column("name", db.String(50))
    type = db.Column("type", db.String(20))
    date = db.Column("date", db.DateTime)



