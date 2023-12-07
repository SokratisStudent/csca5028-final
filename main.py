from flask import request, render_template, url_for, redirect

from datetime import datetime

from webapp.src.init_app import create_app
from components.database.main import db
from components.person.src.person_db_model import Person
from components.person.src.person_control import createPerson, parseVacationsRequest, createVacations, PersonalVacationObj
from components.public_holidays.src.public_holiday_control import getHolidays
from components.project.src.project_control import getActiveProjects, createProject

app = create_app(db)
current_person: Person
current_vacations_requested: list[PersonalVacationObj] = []

@app.route("/")
def main():
    return render_template("index.html")


@app.route("/projects")
def projects():
    return render_template("projects.html", projects=getActiveProjects())


@app.route("/person")
def person():
    return render_template("person.html")


@app.route("/vacationEmail")
def vacation_email():
    return render_template("vacation_email.html")


@app.route("/vacationEmail/display", methods=["POST"])
def vacation_email_parse():
    email_text = request.form.get("email_text", "")

    global current_person
    global current_vacations_requested
    current_person, current_vacations_requested = parseVacationsRequest(email_text)

    if current_person == None:
        return render_template("error.html", error_message=f'Could not identify an existing entry in the system for the person asking for vacation! Please add the person before trying to add vacation time for them.')

    table_html = (f'<p> Email analysis indicates the below vacations will be taken: ' +
            '</p><table style="width:30%"><tr><th style="width:50%">Name</th><th>Date from</th><th>Date to</th></tr>')

    for vacation in current_vacations_requested:
        table_html += f'<tr><td>{vacation.name}</td><td>{vacation.start_date}</td><td>{vacation.end_date}</td></tr>'

    table_html += '</table>'

    return render_template('email_parse.html', vacations=current_vacations_requested)


@app.route("/vacationEmail/process", methods=["POST"])
def vacation_email_accept():
    accept_result = request.form.get('accept')
    reject_result = request.form.get('reject')

    global current_person
    global current_vacations_requested

    if accept_result == "Accept" and reject_result is None and current_person is not None and len(current_vacations_requested) > 0:
        createVacations(current_person, current_vacations_requested)
        current_person = None
        current_vacations_requested = []

    return render_template("index.html")


@app.route("/createPerson", methods=["POST"])
def add_person():
    name = request.form.get("name", "")
    country = request.form.get("country", "")

    new_person = createPerson(name, country)
    if new_person is None:
        return render_template("error.html", error_message=f'{name} already exists in the database!')

    holidays = getHolidays(country)

    return_html = (f'<p>Created {new_person.name} working in {new_person.country_name} with the following holidays: ' +
                   '</p><table style="width:30%"><tr><th style="width:80%">Name</th><th>Date</th></tr>')

    for holiday in holidays:
        return_html += f'<tr><td>{holiday.name}</td><td>{holiday.date:%d-%m-%Y}</td></tr>'

    return_html += '</table>'

    return return_html


@app.route("/createProject", methods=["POST"])
def add_project():
    project_name = request.form.get("project_name", "")

    if createProject(project_name) is False:
        return render_template("error.html", error_message=f'{project_name} already exists in the database!')

    return redirect(url_for('projects'))


