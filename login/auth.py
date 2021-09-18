import json
import hashlib
import os
import validator
import string
import random
from bson import ObjectId
from dotenv import load_dotenv
from db import user,user_session


env_path = 'config1.env'
load_dotenv(dotenv_path=env_path)



class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)


async def insert_val(json):

    user_session.insert_one(json)


async def login_func(emailId, password, user_agent):

    hashed_password = hashlib.pbkdf2_hmac('sha512', bytes(password, 'utf-8'), bytes(os.environ.get("salt"), 'utf-8'),
                                          int(os.environ.get("iterations"))).hex()

    print("emailId", emailId)
    print('hashed_password', hashed_password)
    print('user_agent', user_agent)

    fetched_records = user.find({"emailId": emailId})

    records = [record for record in fetched_records]
    print(records)

    if not records == []:

        for record in records:

            if record['emailId'] == emailId and record['password'] == hashed_password:
                token = "Bearer " + await random_token()
                await insert_val({"user_id": record['_id'],
                                  "token": token,
                                  "user_agent": user_agent})
                response = {'response': {'token': token, 'user id': eval(str(JSONEncoder().encode(record['_id'])))},
                            'status': 'success'}
                return response

            else:
                email = record['emailId'] == emailId
                print("email", email)
                passw = record['password'] == password
                response = {"response": {"status": "failed", "message": "validator.InvalidAuthentication",
                                         'error_code': validator.get_ErrorCode('validator.InvalidAuthentication')}}
                if passw == False:
                    response['response']['property_error'] = "check your password"
                return response
    else:
        response = {"response": {"status": "failed", "message": "validator.InvalidAuthentication",
                                 'error_code': validator.get_ErrorCode('validator.InvalidAuthentication'),
                                 'property_error': "check your emailId"}}
        return response


async def random_token(size=int(os.environ.get("token_size")),
                       chars=string.ascii_uppercase + string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))
