import sqlalchemy.exc

from components.database.main import db
from components.project.src.project_model import Project


def createProject(name: str) -> bool:
    project_entry = Project(name=name)
    try:
        db.session.add(project_entry)
        db.session.commit()
        return True
    except sqlalchemy.exc.IntegrityError:
        db.session.rollback()
        return False


def getActiveProjects() -> list[Project]:
    return Project.query.all()
