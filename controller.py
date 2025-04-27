from flask import request, jsonify, send_file
from model import Model
import cv2
import numpy as np
import io
from ultralytics import YOLO

class Controller:
    def __init__(self, app_instance):
        self._app = app_instance
        self.__db_model = Model()
        self.__yolo_model = YOLO('best.pt')
        self.__image = ''


        self._setup_routes()

    def _setup_routes(self):
        self._app.add_url_rule('/post/image', view_func=self._post_image, methods=['POST'])
        self._app.add_url_rule('/get/image', view_func=self._get_image, methods=['GET'])
        self._app.add_url_rule('/insert/data', view_func=self._insert_data, methods=['POST'])
        self._app.add_url_rule('/find/data', view_func=self._find_data, methods=['GET'])

    def _post_image(self):
        try:
            image_bytes = request.data
            nparr = np.frombuffer(image_bytes, np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

            results = self.__yolo_model(img, verbose=False, conf=0.5)
            detected_frame = results[0].plot()

            _, img_encoded = cv2.imencode('.jpg', detected_frame)
            img_bytes_io = io.BytesIO(img_encoded.tobytes())

            self.__image = img_bytes_io.getvalue()

            return jsonify({"message": "Image processed and uploaded successfully!"}), 200

        except Exception as e:
            return str(e), 500
        
    
    def _get_image(self):
        try:
            return send_file(io.BytesIO(self.__image), mimetype='image/jpeg')
        except Exception as e:
            return str(e), 500



    def _insert_data(self):
        try:
            data = request.get_json()
            ph = data.get('ph')
            soil = data.get('soil')
            self.__db_model.insert_data(ph, soil)

            return jsonify({'message': 'Data saved successfully'}), 201
        except Exception as e:
            return str(e), 500

    def _find_data(self):
        try:
            data = self.__db_model.find_data()
            return jsonify(data), 200
        except Exception as e:
            return str(e), 500

    def run(self):
        self._app.run(host='0.0.0.0')
