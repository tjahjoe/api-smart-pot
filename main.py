from controller import Controller
from flask import Flask

if __name__ == '__main__':
    app = Flask(__name__)
    controller = Controller(app)
    controller.run()