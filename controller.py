from flask import Flask, request, jsonify, send_file
import io

class Controller():
    def __init__(self):
        self._app = Flask(__name__)

        self.__image = ''

        self._app.add_url_rule('/post/image', view_func=self._post_image, methods=['POST'])
        self._app.add_url_rule('/get/image', view_func=self._get_image, methods=['GET'])

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

    # def _insert_data(self):
    #     try:
    #         data = request.get_json()
    #         temperature = data.get('temperature')
    #         humidity = data.get('humidity')
    #         air_quality = data.get('air_quality')
    #         motion = data.get('motion')

    #         self.__model.insert_data(temperature, humidity, air_quality, motion)
            
    #         return jsonify({'message': 'Data saved successfully'}), 201
    #     except Exception as e:
    #         return str(e), 500
        
    # def _find_all_data(self):
    #     try:
    #         data = self.__model.find_all_data()
    #         return jsonify(data), 201
    #     except Exception as e:
    #         return str(e), 500
        
        
    def run(self):
        self._app.run(host='0.0.0.0')
