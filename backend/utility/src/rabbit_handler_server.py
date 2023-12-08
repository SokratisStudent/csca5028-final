import json
import pika
from flask import Flask

from datamodel.datamodel import ProjectData, PersonData, AbsenceData, to_json

from backend.project.src.project_control import createProject
from backend.person.src.person_control import createPerson
from backend.project.src.project_control import getActiveProjects, getAllPeopleInProject
from backend.person.src.person_control import createVacations, getAllAbsencesForPerson


class RabbitHandlerServer:
    def __init__(self, app: Flask, test_app: Flask):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='actions')
        self.channel.basic_consume(queue='actions', on_message_callback=self.callback, auto_ack=True)
        self.channel.queue_declare(queue="project_data")
        self.app = app
        self.test_app = test_app

    def start(self):
        with self.app.app_context():
            self.refreshData()

        self.channel.start_consuming()

    def updateData(self, projects: list[ProjectData], people: list[PersonData], absences: list[AbsenceData]):
        message = to_json(projects, people, absences)
        self.channel.basic_publish(exchange="", routing_key="project_data", body=json.dumps(message))
        print(f' [x] Data Refreshed')

    def callback(self, ch, method, properties, body):
        json_object: dict = json.loads(json.loads(body))

        match json_object["request"]:
            case 'add_project':
                print(f' [x] Received add_project request for {json_object["name"]}')
                with self.app.app_context():
                    createProject(json_object["name"])
                    self.refreshData()
            case 'test_add_project':
                print(f' [x] Received test_add_project request for {json_object["name"]}')
                with self.test_app.app_context():
                    createProject(json_object["name"])
            case 'add_person':
                print(f' [x] Received add_person request for {json_object["name"]}, {json_object["country"]}, {json_object["project"]}')
                with self.app.app_context():
                    createPerson(json_object["name"], json_object["country"], json_object["project"])
            case 'test_add_person':
                print(f' [x] Received test_add_person request for {json_object["name"]}, {json_object["country"]}, {json_object["project"]}')
                with self.test_app.app_context():
                    createPerson(json_object["name"], json_object["country"], json_object["project"])

            case _:
                print(" [x] Received %r" % body)

    def refreshData(self):
        project_list: list[ProjectData] = []
        people_list: list[PersonData] = []
        absence_list: list[AbsenceData] = []

        projects = getActiveProjects()
        for project in projects:
            project_list.append(ProjectData(id=project.id, name=project.name))
            people = getAllPeopleInProject(project.id)
            for person in people:
                people_list.append(PersonData(id=person.id, name=person.name, country_code=person.country_code, country_name=person.country_name, project_id=project.id))
                vacations = getAllAbsencesForPerson(person)
                absence_list += [AbsenceData(person_id=person.id, date=vacation.date()) for vacation in vacations]

        self.updateData(project_list, people_list, absence_list)



