import json
import datetime
from dataclasses import dataclass


class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ProjectData):
            return obj.to_dict()
        elif isinstance(obj, PersonData):
            return obj.to_dict()
        elif isinstance(obj, AbsenceData):
            return obj.to_dict()
        return super().default(obj)


@dataclass
class ProjectData:
    id: int
    name: str

    def to_dict(self):
        return {"id": self.id,"name": self.name}


@dataclass
class PersonData:
    id: int
    name: str
    country_code: str
    country_name: str
    project_id: int

    def to_dict(self):
        return {"id": self.id, "name": self.name, "country_code": self.country_code, "country_name": self.country_name, "project_id": self.project_id}


@dataclass
class AbsenceData:
    person_id: int
    date: datetime.date

    def to_dict(self):
        return {"person_id": self.person_id, "date": self.date}


def to_json(projects: list[ProjectData], people: list[PersonData], absences: list[AbsenceData]) -> json:
    proj_json = json.dumps(projects, cls=CustomEncoder)
    ppl_json = json.dumps(people, cls=CustomEncoder)
    abs_json = json.dumps(absences, cls=CustomEncoder)

    return f'{ {proj_json}, {ppl_json}, {abs_json} }'
