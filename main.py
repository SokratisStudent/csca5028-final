from flask import request, render_template

from datetime import datetime

from webapp.app import create_app
from components.database.main import db
from components.public_holidays.src.public_holiday_control import getHolidays

app = create_app(db)


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

    holidays = getHolidays(country, datetime.now().year)

    return_html = (f'<p>Created {name} working in {country} with the following holidays: ' +
                   '</p><table style="width:30%"><tr><th style="width:80%">Name</th><th>Date</th></tr>')

    for holiday in holidays:
        return_html += f'<tr><td>{holiday.name}</td><td>{holiday.date:%d-%m-%Y}</td></tr>'

    return_html += '</table>'

    return return_html


@app.route("/getCountry", methods=["GET"])

@app.route("/viewPerson", methods=["GET"])
def view_person():
    pass

