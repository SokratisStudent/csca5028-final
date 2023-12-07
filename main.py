from flask import request, render_template

from datetime import datetime

from webapp.src.init_app import create_app
from components.database.main import db
from components.personal_vacations.src.person_control import createPerson, parseVacationsRequest
from components.public_holidays.src.public_holiday_control import getHolidays

app = create_app(db)


@app.route("/")
def main():
    return render_template("index.html")


@app.route("/projects")
def projects():
    return render_template("projects.html")


@app.route("/person")
def person():
    return render_template("person.html")


@app.route("/vacationEmail")
def vacation_email():
    return render_template("vacation_email.html")


@app.route("/vacationEmail/process", methods=["POST"])
def vacation_email_parse():
    email_text = request.form.get("email_text", "")

    vacations_requested = parseVacationsRequest(email_text)

    table_html = (f'<p> Email analysis indicates the below vacations will be taken: ' +
                   '</p><table style="width:30%"><tr><th style="width:50%">Name</th><th>Date from</th><th>Date to</th></tr>')

    for vacation in vacations_requested:
        table_html += f'<tr><td>{vacation.name}</td><td>{vacation.start_date}</td><td>{vacation.end_date}</td></tr>'

    table_html += '</table>'

    return render_template('email_parse.html', vacations=vacations_requested)


#@app.route("/createProject", methods=["POST"])
#def add_project():
#    project_name = request.form.get("project_name", "")
#    return "Successfully created " + project_name + " project."


@app.route("/createPerson", methods=["POST"])
def add_person():
    name = request.form.get("name", "")
    country = request.form.get("country", "")

    new_person = createPerson(name, country)
    holidays = getHolidays(country)

    return_html = (f'<p>Created {new_person.name} working in {new_person.country_name} with the following holidays: ' +
                   '</p><table style="width:30%"><tr><th style="width:80%">Name</th><th>Date</th></tr>')

    for holiday in holidays:
        return_html += f'<tr><td>{holiday.name}</td><td>{holiday.date:%d-%m-%Y}</td></tr>'

    return_html += '</table>'

    return return_html


