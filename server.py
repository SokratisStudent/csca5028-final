import sys

from backend.database.main import db
from backend.utility.src.init_app import create_app, create_test_app
from backend.utility.src.rabbit_handler_server import RabbitHandlerServer

if __name__ == '__main__':
    app = create_app(db)
    test_app = create_test_app(db)
    request_receiver = RabbitHandlerServer(app, test_app)
    print("Backend Ready")

    try:
        request_receiver.start()
    except KeyboardInterrupt:
        print('Interrupted')
        sys.exit(0)
