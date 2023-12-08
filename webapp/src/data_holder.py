import json

from datamodel.datamodel import ProjectData, PersonData, AbsenceData


class DataHolder:
    def __init__(self):
        self.projects: list[ProjectData] = []
        self.people: list[PersonData] = []
        self.absences: list[AbsenceData] = []

    def refresh(self, json_data: json):
        print('project_data is refreshing')
        proj_json = json_data[0]
        self.projects = json.loads(proj_json)
        print(self.projects)

    def getActiveProjects(self) -> list[ProjectData]:
        return self.projects

    def getProjectByName(self, name: str) -> ProjectData:
        for project in self.projects:
            if project.name == name:
                return project

    def getAllPeopleInProject(self, project_name: str) -> list[PersonData]:
        project = self.getProjectByName(project_name)
        return [person for person in self.people if person.project_id == project.id]

