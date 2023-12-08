import json
import pika

from webapp.src.data_holder import DataHolder


class RabbitRequestSender:
    def __init__(self, data_holder: DataHolder):
        self.data_holder = data_holder

        self.conn = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
        self.channel = self.conn.channel()
        self.channel.queue_declare(queue="actions")
        self.channel.queue_declare(queue="project_data")
        self.channel.basic_consume(queue='project_data', on_message_callback=self.callback, auto_ack=True)

    def callback(self, ch, method, properties, body):
        print('project_data is arriving')
        json_object: dict = json.loads(json.loads(body))
        self.data_holder.refresh(json_object)

    def createProject(self, project_name: str, test_mode: bool = False) -> bool:
        if test_mode:
            message = json.dumps({"request": "test_add_project", "name": project_name})
        else:
            message = json.dumps({"request": "add_project", "name": project_name})
        try:
            self.channel.basic_publish(exchange="", routing_key="actions", body=json.dumps(message))
        except pika.exceptions.UnroutableError:
            return False

        return True

    def createPerson(self, name: str, country: str, project_name: str, test_mode: bool = False) -> bool:
        if test_mode:
            message = json.dumps({"request": "add_person", "name": name, "country": country, "project": project_name})
        else:
            message = json.dumps({"request": "add_person", "name": name, "country": country, "project": project_name})
        try:
            self.channel.basic_publish(exchange="", routing_key="actions", body=json.dumps(message))
        except pika.exceptions.UnroutableError:
            return False

        return True


