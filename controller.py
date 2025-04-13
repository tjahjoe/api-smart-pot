from flask import request, jsonify, send_file
from data import Data
import io

class Controller():
    def __init__(self, app_instance):
        self._app = app_instance
        self.__image = ''
        self.__data = Data()
        self._app.add_url_rule('/post/image', view_func=self._post_image, methods=['POST'])
        self._app.add_url_rule('/get/image', view_func=self._get_image, methods=['GET'])
        self._app.add_url_rule('/', view_func=self._tes, methods=['GET'])

    def _post_image(self):
        try:
            self.__image = request.data
            return jsonify({"message": "Image received successfully!"}), 200
        except Exception as e:
            return str(e), 500

    def _get_image(self):
        try:
            return send_file(io.BytesIO(self.__image), mimetype='image/jpeg')
        except Exception as e:
            return str(e), 500

    def _tes(self):
        try:
            return jsonify({'message': self.__data.data}), 200
        except Exception as e:
            return str(e), 500

    def run(self):
        self._app.run(host='0.0.0.0')