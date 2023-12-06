from flask import request, render_template

from settings import settings_data
from webapp.app import create_app
from components.database.main import create_db

from components.public_holidays.src.public_holidays_http_request import PublicHolidayRequest

app = create_app()
db = create_db(app)

from components.public_holidays.src.public_holiday_control import getHolidays

with app.app_context():
    db.create_all()

@app.route("/")
def main():

    return render_template("index.html")


#@app.route("/createProject", methods=["POST"])
#def add_project():
#    project_name = request.form.get("project_name", "")
#    return "Successfully created " + project_name + " project."


@app.route("/createPerson", methods=["POST"])
def add_person():
    name = request.form.get("name", "")
    country = request.form.get("country", "")

    holidays = getHolidays(country)

    return "Created " + name + " working in " + country + " with " + str(len(holidays)) + " holidays"

@app.route("/getCountry", methods=["GET"])

@app.route("/viewPerson", methods=["GET"])
def view_person():
    pass

