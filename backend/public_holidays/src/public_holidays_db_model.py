from backend.database.main import db


class PublicHoliday(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    country_code = db.Column(db.String(2), db.ForeignKey('country.country_code'))
    name = db.Column("name", db.String(50))
    type = db.Column("type", db.String(20))
    date = db.Column("date", db.DateTime)



