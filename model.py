from pymongo import MongoClient
from pymongo.server_api import ServerApi
from datetime import datetime
import pandas as pd
import os

class Model():
    def __init__(self):
        # self.__client = MongoClient(os.environ.get("MONGODB_API"),  server_api=ServerApi('1'))
        self.__client = MongoClient('mongodb+srv://elchilz:Elco1001@smartfarm.zrqtr.mongodb.net/?retryWrites=true&w=majority&appName=smartfarm',  server_api=ServerApi('1'))
        self.__url = 'https://res.cloudinary.com/dkozkdqen/image/upload/'
        try:
            self.__database = self.__client.get_database('smartfarm')
            self.__collection()
            self.__specification()
        except Exception as e:
            print(f'Error: {e}')

    def __collection(self):
        self.__collection_data = self.__database.get_collection('data')
        self.__collection_user = self.__database.get_collection('user')
        self.__collection_image = self.__database.get_collection('image')

    def __specification(self):
        self.__collection_user.create_index([('pot_id')], unique=True)

    def insert_user(self, chat_id, pot_id):
        user = {
            'chat_id' : chat_id,
            'pot_id' : pot_id
            }

        self.__collection_user.insert_one(user)
        self.__insert_image(pot_id)


    def is_user(self, pot_id):
        user = self.__collection_user.find_one({'pot_id' : pot_id}, {'_id': 0,'chat_id' : 1}) 
        if user == None:
            return False
        else:
            return True       

    def __insert_image(self, pot_id):
        image = {
            'pot_id' : pot_id,
            'url' : f'{self.__url}{pot_id}'
        }

        self.__collection_image.insert_one(image)


    def find_image(self, pot_id):
        image = self.__collection_image.find_one({'pot_id' : pot_id}, {'_id': 0,'url' : 1})

        if image == None:
            return False
        else:
            return image['url']

    def insert_data(self, ph, soil):
        now = datetime.now()
        year = now.year
        month = now.month
        day = now.day
        hour = now.hour
        minute = now.minute

        data = {
            'year' : year,
            'month' : month,
            'day' : day,
            'hour' : hour,
            'minute' : minute,
            'data' : {
                'ph': ph,
                'soil': soil,
                }
            }
        
        self.__collection_data.insert_one(data)
    
    def find_data(self):
        cursor = self.__collection_data.find({}, {'_id': 0, 'data.ph': 1, 'data.soil': 1}).sort('_id', -1).limit(10)
        raw_data = list(cursor)

        df = pd.json_normalize(raw_data) 

        df = df[['data.ph', 'data.soil']].iloc[::-1]  

        return df.rename(columns={'data.ph': 'ph', 'data.soil': 'soil'}).to_dict(orient='records')