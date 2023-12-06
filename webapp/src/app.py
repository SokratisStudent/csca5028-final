#from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
#from components.public_holidays.public_holidays_http_request import PublicHolidayRequest

#app = Flask(__name__, template_folder='html')
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///vacations.sqlite3'
#db = SQLAlchemy(app)
#db.init_app(app)

#with app.app_context():
#    db.create_all()

#@app.route("/")
#def src():
#    return render_template("index.html")


#@app.route("/createProject", methods=["POST"])
#def add_project():
#    project_name = request.form.get("project_name", "")
#    return "Successfully created " + project_name + " project."


#@app.route("/createPerson", methods=["POST"])
#def add_person():
#    name = request.form.get("name", "")
#    country = request.form.get("country", "")
#    holiday_request = PublicHolidayRequest()
#    holidays = holiday_request.fetch_data("CY", "2024")

    #for new_entry in holidays:
    #    db.session.add(new_entry)
    #db.session.commit()

#    return "Created " + name + " working in " + country
