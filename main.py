from flask import request, render_template, url_for, redirect

from webapp.src.init_app import create_app
from components.database.main import db
from components.person.src.person_db_model import Person
from components.person.src.person_control import createPerson, parseVacationsRequest, createVacations, PersonalVacationObj, getAllAbsencesForPerson
from components.project.src.project_control import getActiveProjects, createProject, getAllPeopleInProject
from components.utility.src.utility import calculate_timespan

app = create_app(db)
current_person: Person = None
current_vacations_requested: list[PersonalVacationObj] = []

@app.route("/")
def main():
    return render_template("index.html")


@app.route("/projects")
def projects(test_mode=False):
    timespan = 90
    days, months, dates = calculate_timespan(timespan)
    output = ""
    active_projects = getActiveProjects()
    for project in active_projects:
        output += f'<table><tr><th width=120>{project.name}</th>'
        for month in months:
            output += f'<th colspan=\"{months[month]}\">{month}</th>'
        output += "</tr><tr><td></td>"
        for day in days:
            output += f'<td>{day:0>2}</td>'
        output += "</tr>"
        people = getAllPeopleInProject(project)
        for employee in people:
            output += "<tr>"
            output += f'<td>{employee.name}</td>'
            absences = getAllAbsencesForPerson(employee)
            for i in range(timespan+1):
                if dates[i].weekday() >= 5:
                    output += f'<td style="background-color: #A0A0A0";></td>'
                elif dates[i] in absences:
                    output += f'<td style="background-color: #A0A0D0";></td>'
                else:
                    output += f'<td style="background-color: #A0D0A0"></td>'
            output += "</tr>"
        output += "</table><br><br>"

    if test_mode:
        return output

    return render_template("projects.html", project_table=output)


@app.route("/person")
def person():
    project_list = getActiveProjects()
    return render_template("person.html", project_list=project_list)


@app.route("/vacationEmail")
def vacation_email():
    return render_template("vacation_email.html")


@app.route("/vacationEmail/display", methods=["POST"])
def vacation_email_parse():
    email_text = request.form.get("email_text", "")

    global current_person
    global current_vacations_requested
    current_person, current_vacations_requested = parseVacationsRequest(email_text)

    if current_person is None:
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
        name = current_person.name
        current_person = None
        current_vacations_requested = []
        return render_template("success.html", success_message=f'Successfully created vacations for {name}')

    return redirect(url_for('/'))


@app.route("/createPerson", methods=["POST"])
def add_person():
    name = request.form.get("name", "")
    country = request.form.get("country", "")
    project_name = request.form.get("project", "")

    new_person = createPerson(name, country, project_name)
    if new_person is None:
        return render_template("error.html", error_message=f'{name} already exists in the database!')

    return render_template("success.html", success_message=f'Successfully created {new_person.name} working in {new_person.country_name} for {project_name}')


@app.route("/createProject", methods=["POST"])
def add_project():
    project_name = request.form.get("project_name", "")

    if createProject(project_name) is False:
        return render_template("error.html", error_message=f'{project_name} already exists in the database!')

    return redirect(url_for('projects'))
