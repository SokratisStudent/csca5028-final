import sqlalchemy.exc

from components.database.main import db
from components.project.src.project_model import Project
from components.person.src.person_db_model import Person


def createProject(name: str) -> Project:
    project_entry = Project(name=name)
    try:
        db.session.add(project_entry)
        db.session.commit()
    except sqlalchemy.exc.IntegrityError:
        db.session.rollback()
        return None

    return project_entry


def getActiveProjects() -> list[Project]:
    return Project.query.all()


def getProjectByName(name: str) -> Project:
    return Project.query.filter_by(name=name).first()


def getAllPeopleInProject(project: Project) -> list[Person]:
    return Person.query.filter_by(project_id=project.id).all()


